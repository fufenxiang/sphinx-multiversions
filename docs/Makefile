# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = _build
VERSIONS      = latest 1.0 2.0

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help makefile


# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
# %: Makefile
# 	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
# REWRITE %: Makefile
%: Makefile
	@for version in $(VERSIONS); \
	do                        \
	$(SPHINXBUILD) -M $@ "$(SOURCEDIR)/$$version" "$(BUILDDIR)/$$version" $(SPHINXOPTS) $(O); \
	done

clean:
	-rm -rf $(BUILDDIR)

