# 本地维护多版本 Sphinx 文档


本文档使用 Python 配置文件实现本地维护多版本 Sphinx 文档。

## 文档目录树

文档目录树如下:

```
docs
├── source
|   ├── 1.0
|   │   ├── conf.py -> use '../conf_common.py'
|   │   ├── index.rst
|   │   ├── _static
|   │   └── _templates -> use '../_templates'
|   │── 2.0
|   │   ├── conf.py -> use '../conf_common.py'
|   │   ├── index.rst
|   │   ├── _static
|   │   └── _templates -> use '../_templates'
|   │── conf_common.py
|   │── sphinx_html_multi_versions.py
|   │── _static
|   └── _templates
|       └── layout.html
|       └── versions.html -> add versions selector for 'sphinx_rtd_theme'
|
|── Makefile -> build cmd
|
└── requirements.txt --> save enviroment packages

```

## 文件说明

上述目录树中：

**1. `Makefile`: Makefile 文件是 Sphinx 编译构建的脚本文件**

```makefile

# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
# 编译框架，sphinx-build
SPHINXBUILD   ?= sphinx-build
# 编译的源码目录：docs/source
SOURCEDIR     = source
# 编译的输出目录：docs/_build
BUILDDIR      = _build
# 编译版本：需要和 source 目录下的版本目录保持一致
# 编译执行时，拼接 SOURCEDIR/VERSIONS 作为指定版本的编译源码目录；拼接 BUILDDIR/VERSIONS 作为指定版本的编译输出目录
# 如：source/1.0 --> _build/1.0
VERSIONS      = latest 1.0 2.0

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help makefile


# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
# 执行 `make html` 命令，循环编译 $(SOURCEDIR) 目录下的文档版本
# sphinx-build -M source/latest _build/latest
# sphinx-build -M source/1.0 _build/1.0
# sphinx-build -M source/2.0 _build/2.0
%: Makefile
	@for version in $(VERSIONS); \
	do                        \
	$(SPHINXBUILD) -M $@ "$(SOURCEDIR)/$$version" "$(BUILDDIR)/$$version" $(SPHINXOPTS) $(O); \
	done

# 执行 `make clean` 命令，移除 $(BUILDDIR) 目录
# rm -rf _build
clean:
	-rm -rf $(BUILDDIR)

```


**2. `docs/source/sphinx_html_multi_versions.py` 是实现 Sphinx 多版本的配置文件，通过 html_context 保存一个版本列表，版本列表中的元素来自于当前目录[source] 下不以 '_' 开头的目录名**

```py
"""
Sphinx HTML Multiple Versions.

Loads the list of versions into the configuration file.
"""

import os

# Get the list of all versions for which a documentation is available
html_context = {"versions": []}
versions_path = os.path.dirname(__file__) + "\\"
# print("========= versions_path: ", versions_path)
for file in os.listdir(versions_path):
    if os.path.isdir(versions_path + file) and file[0] != "_":
        html_context["versions"].append(os.path.basename(file))

```


**3. `docs/source/conf_common.py` 是 Sphinx 各版本编译使用的公共配置文件，该文件需要导入 `docs/source/sphinx_html_multi_versions.py` 来获取版本列表**

```py
...

# 导入同级目录下的 sphinx_html_multi_versions 模块
import sphinx_html_multi_versions
html_context = sphinx_html_multi_versions.html_context
```

**`docs/source/1.0/conf.py` 、`docs/source/2.0/conf.py` 通过导入`docs/source/conf_common.py`同步构建配置**

```py
# source/1.0/conf.py
# source/2.0/conf.py

# 导入上级目录公共配置
import os
import sys
sys.path.insert(0, os.path.abspath('../'))
from conf_common import *

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# 获取当前配置文件所在的目录，即版本路径，如：latest，1.0，2.0
release = os.path.basename(os.path.dirname(__file__))
# The short X.Y version.
version = release

```


**4. `docs/source/_templates/` 目录是模板目录，保存了公共 Layout 和其他所需要的 HTML 文件**

**`docs/source/conf_common.py` 文件中的配置项**

```py
templates_path = [os.path.dirname(os.path.realpath(__file__)) + "\_templates"]
```

**确保各个版本均使用 docs/source/_templates/ 目录作为模板目录**


**_templates/ 目录中还有一个文件 `versions.html`，这是 `sphinx_rtd_theme` 主题的版本选择组件文件。可以看一下`sphinx_rtd_theme` 主题的 layoyt.html 源码，其中有一行：**

```html
<!-- \venv\Lib\site-packages\sphinx_rtd_theme -->

...

{% include "versions.html" -%}

...

```

**因此，创建 `versions.html` 文件为 `sphinx_rtd_theme` 主题添加版本选择器。**

```html
<!-- Add versions dropdown selector for sphinx_rtd_theme 
    Keep file name as versions.html, do not change.
-->
<div class="rst-versions" data-toggle="rst-versions" role="note" aria-label="versions">
    <span class="rst-current-version" data-toggle="rst-current-version">
      <span class="fa fa-book"> Sphinx Multiple Versions</span>
      V: {{ release }}
      <span class="fa fa-caret-down"></span>
    </span>
    <div class="rst-other-versions">
        <dl>
        {% for version in versions %}
        <!-- a 标签跳转: 用当前选择的版本替换 url 中的版本 -->
        <dd><a href="javascript:void(0)" onclick="location.href = location.href.replace('/{{ release }}', '/{{ version }}');">{{ version }}</a></dd>
        {% endfor %}
      </dl>
    </div>
</div>

```

## 编译构建


**1. 每个版本可以单独构建的，编译命令中应指定源文件以及输出目录，例如:**

```py
# 在 docs/ 目录下
# 编译 1.0 版本
sphinx-build -b html source/1.0 _build_/1.0
# 编译 2.0 版本
sphinx-build -b html source/2.0 _build_/2.0
```

编译完成后在 `docs/_build` 目录下生成编译输出。



**2. 使用 Makefile 文件一次性编译所有版本**

```py
# 在 docs/ 目录下执行：
 make html
```

编译完成后在 `docs/_build` 目录下生成编译输出。


## 非常重要的小提示

**1. 如果只有某一个版本的文档更新，只需要单独编译该版本即可；**

**2. 如果新增一个版本或删除一个版本，则需要重新编译生成所有版本，否则历史版本的版本选择器不会更新；**

