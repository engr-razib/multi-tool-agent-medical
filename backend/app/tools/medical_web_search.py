
import requests

class MedicalWebSearchTool:
    name = "MedicalWebSearchTool"
    description = "Search PubMed and Wikipedia for general medical knowledge (definitions, symptoms, treatments)."

    def search_pubmed(self, query, retmax=5):
        base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        params = {"db": "pubmed", "term": query, "retmode": "json", "retmax": retmax}
        r = requests.get(base, params=params, timeout=10)
        data = r.json()
        ids = data.get("esearchresult", {}).get("idlist", [])
        if not ids:
            return []
        sum_base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        r2 = requests.get(sum_base, params={"db":"pubmed","id":",".join(ids),"retmode":"json"}, timeout=10)
        summ = r2.json().get("result", {})
        res = []
        for _id in ids:
            doc = summ.get(_id, {})
            if doc:
                res.append({"id": _id, "title": doc.get("title"), "source": "PubMed"})
        return res

    def search_wikipedia(self, query):
        base = "https://en.wikipedia.org/w/api.php"
        params = {"action":"opensearch","search":query,"limit":3,"namespace":0,"format":"json"}
        r = requests.get(base, params=params, timeout=8)
        data = r.json()
        titles = data[1]
        descs = data[2]
        links = data[3]
        return [{"title": t, "snippet": s, "link": l} for t, s, l in zip(titles, descs, links)]

    def run(self, user_query: str) -> str:
        q = user_query.lower()
        if any(w in q for w in ["definition","what is","symptoms","cure","treatment","diagnosis","how to treat"]):
            pub = self.search_pubmed(user_query)
            if pub:
                return "PubMed top results:\n" + "\n".join([f"- {p['title']} (id:{p['id']})" for p in pub])
            wiki = self.search_wikipedia(user_query)
            if wiki:
                return "Wikipedia quick results:\n" + "\n".join([f"- {w['title']}: {w['snippet']} — {w['link']}" for w in wiki])
            return "No results found on PubMed or Wikipedia."
        else:
            pub = self.search_pubmed(user_query)
            if pub:
                return "PubMed top results:\n" + "\n".join([f"- {p['title']} (id:{p['id']})" for p in pub])
            return "No immediate results."
