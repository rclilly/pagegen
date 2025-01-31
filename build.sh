#!/bin/bash

# Create new release

set -e

build_dir='/home/oliver/Documents/Projects/pagegen'

cd "$build_dir"


# Update version in setup.py

current_version="$(grep "^\s*version='" setup.py)"
current_version="${current_version/version=\'/}"
current_version="${current_version/\',/}"
current_version="${current_version#"${current_version%%[![:space:]]*}"}"


echo "Keep current version number $current_version? [y|n]"
read keep_version

if [ "$keep_version" = "n" ]; then
	echo "Enter new version number:" 
	read build_version

	sed -i "s/version='$current_version'/version='$build_version'/" setup.py
elif [[ "$keep_version" = "y" ]] || [[ "$keep_version" = "" ]]; then
	build_version="$current_version"
else
	echo "Unable to understand '$keep_version', quitting.."
	exit 1
fi


# Clean old builds
python3 setup.py clean --all
rm -Rf dist


# Build package
python3 setup.py bdist_wheel

package="$PWD/dist/pagegen-${build_version}-py3-none-any.whl"


# Test it?
echo
echo "Care to do some interactive testing? [y|n]"
read do_test

if [ "$do_test" = "y" ]; then
	

	test_dir="$(mktemp -d)"
	pg_dir="test_site"
	trap 'rm -rf -- "$test_dir"' EXIT
	cd "$test_dir"

	# Setup virtualenv for testing
	mkdir venv
	virtualenv venv
	. venv/bin/activate
	pip install "$package"

	# Init pagegen test site
	mkdir "$pg_dir"
	cd "$pg_dir"
	pagegen --init

	echo
	echo "Starting test environment, type exit to continue build.."
	echo
	bash --norc -i # Create subshell with same env as current

	deactivate
fi


# Upload to pypi
echo "Package built, upload it to pypi? [y|n]"
read release
if [ "$release" = "y" ]; then
	twine upload "$package"
fi

echo "Build done, remember to create github release"
