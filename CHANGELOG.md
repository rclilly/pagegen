# v3.?.?

## Added

- strip_extensions site.conf setting removes defined file extensions in generated output. Extensions may be comma separated

## Fixed

- pagegen command line argument --production <version> now works, fixes https://github.com/oliverfields/pagegen/issues/14


# v3.8.0

## Removed

- Page Category functionality, it was basically same as tags, so removed duplicate code

## Fixed

- Incompatibility with markdown version after 3.3.6, so locked pip package to last known working version

# v3.7.1

## Fixed

- Custom headers where being converted in hook/script environments, now they are just strings
- Shortcodes __repr__ now uses inspect.signature, supports auto documenting shortcodes with \*args and \*\*kwargs



# OLD STYLE LOG:


## v3.7.0 - 2022-03-24

## Added

- Shortcodes, define regular python functions that must reutrn a string in shortcodes.py and use "<sc>shortcode_name(arg1, .. argN)</sc>" in content where you want them, or <% n = shortcodes['name'](site, page, arg1, .. argN) %>${n}" in templates. Disable shortcodes with page header "disable shortcodes: True". See https://pagegen.phnd.net/user-manual/shortcodes
- Authors - add authors csv header to pages and authors.conf to generate author pages
- Excerpts. Use  <!-- more --> anywhere in content and everything until then will become page.excerpt.
- Shortcodes list_posts, tags and categories


## Removed

- page_titles site.conf setting, to add titles to pages, use templates


## v3.6.0 - 2022-01-30

## Added

- Graphviz support for both markdown and rst added
- Title numbering, use page header 'number headings: true'
- TOC for pages, use page header 'toc: True' and page.toc will be available in templates

### Fixed

- Hot reload (--serve) fixed
- Markdown generation fixed
- Asset directory now is copied to outpu


## v3.5.0 - 2022-01-24

### Added

- When using --serve any changes to the site will trigger rebuild. Pages being served will reload if a rebuild has occured. The F5 key will appreciate
- Markdown support, in site.conf set default "markup=md" to use markdown as default, can be overriden in page headers using "Markdown: mk". Default is rst
-


### Fixed

- Pages with header exclude link chain where not being converted to html


### Removed

- Header_profiles functionality


## v3.4.0 - 2022-01-13

### Added

- Mako template engine, now templates can have full power of Mako, incl if else, loops and full on python code execution
- Page headers/frontmatter support custom headers. These can be referenced in templates using format {{page.<header name>}}. Example, if in a page the following header is set 'this is a custom header: At last', then in a template the following '{{page.this is a custom header}}' will be replaced with 'At last'
- Template variable/placeholder page_file_name added, contains what you expect
- Template variable/placeholder page_relative_url added, contains url relative to web root
- Template variable/placeholder default_extension added, contains default file extension

### Fixed

- Template page_file_name was incorrect for directories
- --serve disables deploy and post_deploy hooks for serving locally
- Removed superflous printing
- Sitemaps now have corecct urls
- Hooks now only execute if they have execute rights (linux)


## v3.2.0 - 2021-12-30

### Added

- Added page header Exclude html minify, set to True to disable html minifying of the page
- New command argument -s|--serve <environment>, builds and serves the envionment on localhost, rebuilds if content is changed. Will force base_url to localhos:8000 when serving

### Changed

- Moved deploy_scripts functionality to new deploy hook
- Command line arguments changed. Environment must now be specified with -g or -s. --help argument added

### Fixed

- Executable content files where returning bytes instead of strings, this is python3 behaviour and has been fixed
- Page header preserve file name now is enforced, before the file name could have the default extension added, if specified in site.conf'
- Multiple variable in a line containing : where matching too much


## v3.1.1 - 2021-12-14

### Changed

- pagegen --init now includes examples of scripts


## v3.1.0 - 2021-12-13

### Added

- Custom deploy scripts per environment, currently ftp is supported
- Minify html, css and javascript options

### Changed

- Refactored variable initializing, under the hood..

### Removed

- Upload to FTP functionality. New deploy_scripts/ftp.py are drop in replacement
