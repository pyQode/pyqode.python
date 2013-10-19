def setup(app):
    app.add_crossref_type(
        directivename="jedi",
        rolename="jedi",
        indextemplate="pair: %s; jedi")
