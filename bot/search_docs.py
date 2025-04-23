# search_docs.py
import requests

DOCS_BASE = {
    # Language docs
    "python": "https://devdocs.io/python~3/",
    "javascript": "https://developer.mozilla.org/en-US/search?q=",
    "java": "https://docs.oracle.com/javase/8/docs/api/index.html?search=",
    "c++": "https://en.cppreference.com/mwiki/index.php?search=",
    "c": "https://en.cppreference.com/mwiki/index.php?search=",
    "go": "https://pkg.go.dev/search?q=",
    "ruby": "https://ruby-doc.org/search.html?q=",
    "php": "https://www.php.net/manual-lookup.php?pattern=",
    "rust": "https://doc.rust-lang.org/std/?search=",
    "kotlin": "https://kotlinlang.org/docs/home.html#search",

    # Web dev frameworks
    "react": "https://react.dev/search?q=",
    "vue": "https://vuejs.org/search?q=",
    "angular": "https://angular.io/search?q=",
    "svelte": "https://svelte.dev/search?q=",

    # Backend frameworks
    "flask": "https://flask.palletsprojects.com/en/latest/search/?q=",
    "django": "https://docs.djangoproject.com/en/stable/search/?q=",
    "express": "https://expressjs.com/en/api.html#search=",

    # Machine learning & data
    "pandas": "https://pandas.pydata.org/docs/search.html?q=",
    "numpy": "https://numpy.org/search/?q=",
    "scikit-learn": "https://scikit-learn.org/stable/search.html?q=",
    "tensorflow": "https://www.tensorflow.org/search?query=",
    "pytorch": "https://pytorch.org/search/?q=",
}

def search_docs(language, query):
    language = language.lower()
    query = query.strip().replace(" ", "+")
    
    if language == "python":
        # DevDocs doesn't support search API — just link directly
        return f"{DOCS_BASE['python']}{query}"
    
    elif language in ["js", "javascript"]:
        return f"{DOCS_BASE['javascript']}{query}"
    
    else:
        return " Unsupported language. Try `python` or `javascript`."
