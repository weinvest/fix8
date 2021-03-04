//-----------------------------------------------------------------------------------------
/*

Fix8 is released under the GNU LESSER GENERAL PUBLIC LICENSE Version 3.

Fix8 Open Source FIX Engine.
Copyright (C) 2010-16 David L. Dight <fix@fix8.org>

Fix8 is free software: you can  redistribute it and / or modify  it under the  terms of the
GNU Lesser General  Public License as  published  by the Free  Software Foundation,  either
version 3 of the License, or (at your option) any later version.

Fix8 is distributed in the hope  that it will be useful, but WITHOUT ANY WARRANTY;  without
even the  implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

You should  have received a copy of the GNU Lesser General Public  License along with Fix8.
If not, see <http://www.gnu.org/licenses/>.

BECAUSE THE PROGRAM IS  LICENSED FREE OF  CHARGE, THERE IS NO  WARRANTY FOR THE PROGRAM, TO
THE EXTENT  PERMITTED  BY  APPLICABLE  LAW.  EXCEPT WHEN  OTHERWISE  STATED IN  WRITING THE
COPYRIGHT HOLDERS AND/OR OTHER PARTIES  PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY OF ANY
KIND,  EITHER EXPRESSED   OR   IMPLIED,  INCLUDING,  BUT   NOT  LIMITED   TO,  THE  IMPLIED
WARRANTIES  OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.  THE ENTIRE RISK AS TO
THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH YOU. SHOULD THE PROGRAM PROVE DEFECTIVE,
YOU ASSUME THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

IN NO EVENT UNLESS REQUIRED  BY APPLICABLE LAW  OR AGREED TO IN  WRITING WILL ANY COPYRIGHT
HOLDER, OR  ANY OTHER PARTY  WHO MAY MODIFY  AND/OR REDISTRIBUTE  THE PROGRAM AS  PERMITTED
ABOVE,  BE  LIABLE  TO  YOU  FOR  DAMAGES,  INCLUDING  ANY  GENERAL, SPECIAL, INCIDENTAL OR
CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT
NOT LIMITED TO LOSS OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR
THIRD PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS), EVEN IF SUCH
HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

*/
//-----------------------------------------------------------------------------------------
#include "precomp.hpp"
// f8 headers
#include <fix8/f8includes.hpp>
#include <fix8/usage.hpp>
#include <f8c.hpp>

//-----------------------------------------------------------------------------------------
using namespace std;
using namespace FIX8;

//-----------------------------------------------------------------------------------------
extern string shortName, odir, prefix;
extern bool verbose, nocheck, nowarn, incpath;
extern string spacer, precompHdr;
extern const string GETARGLIST;
extern unsigned glob_errors, glob_warnings;

//-----------------------------------------------------------------------------------------
void print_usage();
int process(XmlElement& xf, Ctxt& ctxt);
int load_fix_version (XmlElement& xf, Ctxt& ctxt);
int load_fields(XmlElement& xf, FieldSpecMap& fspec);
void process_special_traits(const unsigned short field, FieldTraits& fts);
int process_message_fields(const std::string& where, XmlElement *xt, FieldTraits& fts,
	const FieldToNumMap& ftonSpec, FieldSpecMap& fspec, const Components& compon);
int load_messages(XmlElement& xf, MessageSpecMap& mspec, const FieldToNumMap& ftonSpec, FieldSpecMap& fspec);
void process_ordering(MessageSpecMap& mspec);
void process_value_enums(FieldSpecMap::const_iterator itr, ostream& ost_hpp, ostream& ost_cpp);
const string& mkel(const string& base, const string& compon, string& where);
void process_group_ordering(const CommonGroupMap& gm);
unsigned lookup_component(const Components& compon, const f8String& name);
string bintoaschex(const string& from);

//-----------------------------------------------------------------------------------------
namespace
{
	const string ident_set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789");
};

//-----------------------------------------------------------------------------------------
ostream *open_ofile(const string& odir, const string& fname, string& target)
{
	if (!exist(odir))
		return nullptr;
	ostringstream ofs;
	string odirect(odir);
	ofs << CheckAddTrailingSlash(odirect) << fname;
	target = ofs.str();
	unique_ptr<ofstream> os(new ofstream(target.c_str()));
	if (!*os)
	{
		cerr << "Error opening file \'" << target << '\'';
		if	(errno)
			cerr << " (" << strerror(errno) << ')';
		cerr << endl;

		return nullptr;
	}

	return os.release();
}

//-----------------------------------------------------------------------------------------
const string& mkel(const string& base, const string& compon, string& where)
{
	ostringstream ostr;
	ostr << base << '/' << compon;
	return where = ostr.str();
}

//-----------------------------------------------------------------------------------------
const string& filepart(const string& source, string& where)
{
	string::size_type pos(source.find_last_of('/'));
	return pos == string::npos ? where = source : where = source.substr(pos + 1);
}

//-----------------------------------------------------------------------------------------
int load_fix_version (XmlElement& xf, Ctxt& ctxt)
{
	const XmlElement *fix(xf.find("fix"));
	if (!fix)
	{
		cerr << "No fix header element found in " << shortName << endl;
		return -1;
	}

	string major, minor, revision("0"), type("FIX");

	if (!fix->GetAttr("major", major) || !fix->GetAttr("minor", minor))
	{
		cerr << "Missing required attributes (major/minor) from fix header in " << shortName << endl;
		return -1;
	}

	if (!fix->GetAttr("revision", revision))
		fix->GetAttr("servicepack", revision);
	fix->GetAttr("type", type);

	// fix version: <Major:1><Minor:1><Revision:2> eg. 4.2r10 is 4210
	ctxt._version = stoi(major) * 1000 + stoi(minor) * 100 + stoi(revision);
	if (type == "FIX" && ctxt._version < 4000)
	{
		cerr << "Unsupported FIX version " << ctxt._version << " from fix header in " << shortName << endl;
		return -1;
	}

	ostringstream ostr;
	ostr << type << ctxt._version;
	ctxt._systemns = ostr.str();
	if (ctxt._fixns.empty())
		ctxt._fixns = ctxt._systemns;
	ctxt._clname = prefix;

	ostr.str("");
	ostr << type << '.' << major << '.' << minor;
	ctxt._beginstr = ostr.str();

	return 0;
}

//-----------------------------------------------------------------------------------------
void process_special_traits(const unsigned short field, FieldTraits& fts)
{
	switch(field)
	{
	case Common_BeginString:
	case Common_BodyLength:
	case Common_CheckSum:
		fts.set(field, FieldTrait::suppress);	// drop through
	case Common_MsgType:
		fts.set(field, FieldTrait::automatic);
		fts.clear(field, FieldTrait::mandatory);	// don't check for presence
	default:
		break;
	}
}

//-----------------------------------------------------------------------------------------
void process_value_enums(FieldSpecMap::const_iterator itr, ostream& ost_hpp, ostream& ost_cpp)
{
	string typestr;
	if (FieldTrait::get_type_string(itr->second._ftype, typestr).empty())
		return;
	typestr.insert(0, "const ");
	typestr += ' ';

	ost_cpp << typestr << itr->second._name << "_realm[]  " << endl << spacer << "{ ";
	unsigned cnt(0);
	for (RealmMap::const_iterator ditr(itr->second._dvals->begin()); ditr != itr->second._dvals->end(); ++ditr)
	{
		if (cnt)
			ost_cpp << ", ";
		ost_cpp << *ditr->first;
		string transdesc(ditr->second);
		// replace any illegal c++ identifier characters
		InPlaceReplaceInSet(ident_set, transdesc, '_');
		ost_hpp << typestr << itr->second._name << '_';
		if (ditr->first->is_range())
			ost_hpp << (cnt == 0 ? "lower" : "upper");
		else if (transdesc.empty())
			ost_hpp << *ditr->first;
		else
			ost_hpp << transdesc;
		ost_hpp << '(' << *ditr->first << ");" << endl;
		++cnt;
	}
	ost_hpp << "const size_t " << itr->second._name << "_realm_els(" << itr->second._dvals->size() << ");" << endl;
	ost_cpp << " };" << endl;

	ost_cpp << "const char *" << itr->second._name << "_descriptions[]  " << endl << spacer << "{ ";
	cnt = 0;
	for (RealmMap::const_iterator ditr(itr->second._dvals->begin()); ditr != itr->second._dvals->end(); ++ditr)
	{
		if (cnt)
			ost_cpp << ", ";
		ost_cpp << '"' << ditr->second << '"';
		++cnt;
	}
	ost_cpp << " };" << endl;
}

//-----------------------------------------------------------------------------------------
int process_message_fields(const std::string& where, const XmlElement *xt, FieldTraits& fts, const FieldToNumMap& ftonSpec,
	FieldSpecMap& fspec, const Components& compon)
{
	unsigned processed(0);
	XmlElement::XmlSet flist;
	if (xt->find(where, flist))
	{
		for(const auto *pp : flist)
		{
			string fname, required;
			if (pp->GetAttr("name", fname) && pp->GetAttr("required", required))
			{
				FieldToNumMap::const_iterator ftonItr(ftonSpec.find(fname));
				FieldSpecMap::iterator fs_itr;
				if (ftonItr == ftonSpec.end() || (fs_itr = fspec.find(ftonItr->second)) == fspec.end())
				{
					cerr << shortName << ':' << recover_line(*pp) << ": error: Field element missing required attributes" << endl;
					++glob_errors;
					continue;
				}

				string compname;
				unsigned compidx(pp->GetAttr("component", compname) ? lookup_component(compon, compname) : 0);

				// add FieldTrait
				if (!fts.add(FieldTrait(fs_itr->first, fs_itr->second._ftype, pp->GetSubIdx(), required == "Y", false, compidx)))
				{
					if (!nowarn)
						cerr << shortName << ':' << recover_line(*pp) << ": warning: Could not add trait object '" << fname << "' (duplicate ?)" << endl;
					++glob_warnings;
				}
				else
				{
					process_special_traits(fs_itr->first, fts);
					++processed;
					fs_itr->second.set_used();
				}
			}
			else
			{
				cerr << shortName << ':' << recover_line(*pp) << ": error: Field element missing required attributes" << endl;
				++glob_errors;
			}
		}
	}

	return processed;
}

//-----------------------------------------------------------------------------------------
string bintoaschex(const string& from)
{
	ostringstream result;
	for (const auto& cc : from)
		result << uppercase << hex << setw(2) << setfill('0') << static_cast<unsigned short>(cc);
	return "FIX8_" + result.str() + '_';
}

//-----------------------------------------------------------------------------------------
void process_ordering(MessageSpecMap& mspec)
{
	for (const auto& pp : mspec)
	{
		FieldTraitOrder mo;
		for (const auto& ii : pp.second._fields.get_presence())
			mo.insert({&ii});

		unsigned cnt(0);
		for (auto *ii : mo)
			ii->_pos = ++cnt;
	}
}

//-----------------------------------------------------------------------------------------
void process_message_group_ordering(const GroupMap& gm)
{
	for (const auto& pp : gm)
	{
		FieldTraitOrder go;
		for (const auto& ii : pp.second._fields.get_presence())
			go.insert({&ii});

		unsigned gcnt(0);
		for (auto *ii : go)
			ii->_pos = ++gcnt;

		if (!pp.second._groups.empty())
			process_message_group_ordering(pp.second._groups);
	}
}

//-----------------------------------------------------------------------------------------
void process_group_ordering(const CommonGroupMap& globmap)
{
	for (const auto& pp : globmap)
      for (const auto& ii : pp.second)
			process_message_group_ordering(ii.second._groups);
}

//-----------------------------------------------------------------------------------------
void print_usage()
{
	UsageMan um("f8c", GETARGLIST, "<input xml schema>");
	um.setdesc("f8c -- compile FIX xml schema");
	um.add('o', "odir <dir>", "output target directory (default ./)");
	um.add('p', "prefix <prefix>", "output filename prefix (default Myfix)");
	um.add('H', "pch <filename>", "use specified precompiled header name for Windows (default none)");
	um.add('d', "dump", "dump 1st pass parsed source xml file, exit");
	um.add('e', "extension", "Generate with .cxx/.hxx extensions (default .cpp/.hpp)");
	um.add('f', "fields", "generate code for all defined fields even if they are not used in any message (default no)");
	um.add('F', "xfields", "specify additional fields with associated messages (see documentation for details)");
	um.add('h', "help", "help, this screen");
	um.add('i', "ignore", "ignore errors, attempt to generate code anyhow (default no)");
	um.add('k', "keep", "retain generated temporaries even if there are errors (.*.tmp)");
	um.add('v', "version", "print version, exit");
	um.add('I', "info", "print package info, exit");
	um.add('s', "second", "2nd pass only, no precompile (default both)");
	um.add('S', "noshared", "Treat every group as unique and expose all static traits. Do not share metadata in message classes (default shared)");
	um.add('N', "nounique", "do not enforce unique field parsing (default false)");
	um.add('R', "norealm", "do not generate realm constructed field instantiators (default false)");
	um.add('W', "nowarn", "suppress warning messages (default false)");
	um.add('C', "nocheck", "do not embed version checking in generated code (default false)");
	um.add('D', "defaulted", "do not generate default router bodies. Application must provide all router definitions (default false)");
	um.add('U', "noconst", "Generate non-const Router method declarations (default false, const)");
	um.add('u', "unused", "Report unused fields, requires verbose option (default false)");
	um.add('r', "retain", "retain 1st pass code (default delete)");
	um.add('b', "binary", "print binary/ABI details, exit");
	um.add('P', "incpath", "prefix system include path with \"fix8\" in generated compilation units (default yes)");
	um.add('c', "classes <server|client>", "generate user session classes (default neither)");
	um.add('t', "tabwidth", "tabwidth for generated code (default 3 spaces)");
	um.add('x', "fixt <file>", "For FIXT hosted transports or for FIX5.0 and above, the input FIXT schema file");
	um.add('V', "verbose", "be more verbose when processing");
	um.add('n', "namespace <ns>", "namespace to place generated code in (default FIXMmvv e.g. FIX4400)");
	um.add("e.g.");
	um.add("@f8c -p Texfix -n TEX myfix.xml");
	um.add("@f8c -rp Texfix -n TEX -x ../schema/FIXT11.xml myfix.xml");
	um.add("@f8c -p Texfix -n TEX -c client -x ../schema/FIXT11.xml myfix.xml");
	um.add("@f8c -p Texfix -n TEX -c client -x ../schema/FIXT11.xml myfix.xml -F \"<field number='9999' name='SampleUserField' type='STRING' messages='NewOrderSingle:Y ExecutionReport:Y OrderCancelRequest:N' />");
	um.print(cerr);
}

//-------------------------------------------------------------------------------------------------
RealmObject *RealmObject::create(const string& from, FieldTrait::FieldType ftype, bool isRange)
{
	if (FieldTrait::is_int(ftype))
		return new TypedRealm<int>(stoi(from), isRange);
	if (FieldTrait::is_char(ftype))
		return new CharRealm(from[0], isRange);
	if (FieldTrait::is_float(ftype))
		return new TypedRealm<fp_type>(get_value<fp_type>(from), isRange);
	if (FieldTrait::is_string(ftype))
		return new StringRealm(from, isRange);
	return nullptr;
}

//-------------------------------------------------------------------------------------------------
string insert_year()
{
   struct tm *ptim;
   time_t now(time(0));
#ifdef _MSC_VER
   ptim = localtime (&now);
#else
   struct tm tim;
   localtime_r(&now, &tim);
   ptim = &tim;
#endif

	ostringstream ostr;
	ostr << setw(2) << (ptim->tm_year - 100);
	return ostr.str();
}

//-------------------------------------------------------------------------------------------------
void generate_includes(ostream& to)
{
	static const vector<string> incfiles
	{
		//"f8includes.hpp"
		"f8exception.hpp",
		"hypersleep.hpp",
		"mpmc.hpp",
		"thread.hpp",
		"f8types.hpp",
		"f8utils.hpp",
		"tickval.hpp",
		"logger.hpp",
		"traits.hpp",
		"field.hpp",
		"message.hpp"
	};

	to << "// f8 includes" << endl;
	for (const auto& pp : incfiles)
		to << "#include " << (incpath ? "<fix8/" : "<") << pp << '>' << endl;
}

//-------------------------------------------------------------------------------------------------
ostream& FIX8::operator<<(ostream& os, const MessageSpec& what)
{
	os << "Name:" << what._name;
	if (!what._description.empty())
		os << " Description:" << what._description;
	if (!what._comment.empty())
		os << " Comment:" << what._comment;
	os << " isadmin:" << boolalpha << what._is_admin << endl;
	os << "Fields:" << endl << what._fields;
	for (const auto& pp : what._groups)
		os << "Group (" << pp.first << "): " << endl << pp.second << endl;

	return os;
}

