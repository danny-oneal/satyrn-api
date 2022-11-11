'''
This file is part of Satyrn.
Satyrn is free software: you can redistribute it and/or modify it under 
the terms of the GNU General Public License as published by the Free Software Foundation, 
either version 3 of the License, or (at your option) any later version.
Satyrn is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with Satyrn. 
If not, see <https://www.gnu.org/licenses/>.
'''

from sqlalchemy import func
from . import utils

def runAutocomplete(db, theType, config, extractor, targetEntity, opts={"query": None}):
    # opts["type"] = config["acType"] if "acType" in config else theType
    # TODO: come back and make this work with multi hop joins
    opts["model"] = config["model"]
    opts["vals"] = config["fields"] if "fields" in config else None
    if not opts["query"] or not opts["vals"]:
        return None
    opts["limit"] = opts["limit"] if "limit" in opts else 1000
    opts["format"] = opts["format"] if "format" in config else ("{} "*len(opts["vals"])).strip()
    sess = db.Session()
    return getDedupedBundle(db, extractor, targetEntity, theType, opts, sess)

# a helper for deduping types that have same names
# this helper is not memoized, though the functions that call into should be
def getDedupedBundle(db, extractor, targetEntity, theType, opts={"query": None}, sess=None):
    if not sess:
        return None

    # targetModel = opts["model"]
    # put together the query
    field, name, joins = utils._get(extractor, targetEntity, theType, db)
    query = sess.query(field)

    if opts["query"]:
        query = query.filter(field.contains(func.lower(opts["query"]))).limit(opts["limit"])

    # TODO: deal with the fact that stuff gets GORY when you just blindly join the strings in a result set
    # Need some representation of how to format each result/entity (like judge name formatting, but in a template string format)
    # in the meantime, just return the first item in the list for the sake of keeping the demo path good
    # later, come back and improve this next line with the template string:
    # output = list(set([" ".join(item) for item in theSet.all()]))
    output = list(set([item[0] for item in query.all()]))
    output.sort()
    return output
