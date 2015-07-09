
from pyld import jsonld
from pyld.jsonld import compact, expand, frame
import json

# Stop code from looking up the contexts online EVERY TIME
def load_document_local(url):
    doc = {
        'contextUrl': None,
        'documentUrl': None,
        'document': ''
    }
    if url == "http://iiif.io/api/presentation/2/context.json":
        fn = "contexts/context_20.json"
    elif url in ["http://www.w3.org/ns/oa.jsonld","http://www.w3.org/ns/oa-context-20130208.json"]:
    	fn = "contexts/context_oa.json"
    else:
        fn = "contexts/context_10.json"
    fh = file(fn)
    data = fh.read()
    fh.close()
    doc['document'] = data;
    return doc

jsonld.set_document_loader(load_document_local)


# Load our (very simple) frame
fh = file('contexts/annotation_frame.json')
data = fh.read()
fh.close()
annoframe = json.loads(data)

# Output Context URI
contextURI = "http://www.w3.org/ns/oa-context-20130208.json"

def convert(anno):
    # check we're already parsed
    if not type(anno) == dict:
        anno = json.loads(anno)
    # rdf = expand(anno)
    reframed = frame(anno, annoframe)
    outjs = compact(reframed, contextURI)
    return outjs


if __name__ == "__main__":
    # Read example from the spec
    fh = file('example_iiif_anno.json')
    data = fh.read()
    fh.close()

    # And convert to OA
    out = convert(data)
    print json.dumps(out, sort_keys=True, indent=2)


