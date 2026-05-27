.ONESHELL:
.PHONY: isort black jacobus toml_sorted beautify commit clean build upload pypi test version works

works:
	@conda env list | awk '{print $$1}' | grep -qx 'works' \
	|| conda create --name works --yes --channel conda-forge --override-channels python=3.11;

isort: works
	conda run -n works pip install 'isort>=6.0,<7';
	conda run -n works isort . ;

black: works
	conda run -n works pip install 'black>=24.5,<26';
	conda run -n works black --line-length=79 . ;

jacobus: works
	conda run -n works pip install 'jacobus>=1.0,<2';
	conda run -n works python -m jacobus . --indent=4 '--f=**/*.cfg' '--f=**/*.css' '--f=**/*.html' '--f=**/*.in' '--f=**/*.js' '--f=**/*.json' '--f=**/*.rst' '--f=**/*.toml' '--f=**/*.txt' '--f=**/*.typed' '--f=**/*.py' '--f=**/.gitignore' '--f=**/Makefile'

toml_sorted: works
	conda run -n works pip install 'toml_sorted>=1.0,<2';
	conda run -n works python -m toml_sorted --infile=pyproject.toml --outfile=pyproject.toml
	conda run -n works python -m toml_sorted --infile=pyproject.toml --key=build-system --outfile=pyproject.toml
	conda run -n works python -m toml_sorted --infile=pyproject.toml --key=build-system --key=requires --outfile=pyproject.toml
	conda run -n works python -m toml_sorted --infile=pyproject.toml --key=project --outfile=pyproject.toml
	conda run -n works python -m toml_sorted --infile=pyproject.toml --key=project --key=classifiers --outfile=pyproject.toml
	conda run -n works python -m toml_sorted --infile=pyproject.toml --key=project --key=dependencies --outfile=pyproject.toml
	conda run -n works python -m toml_sorted --infile=pyproject.toml --key=project --key=urls --outfile=pyproject.toml
	conda run -n works python -m toml_sorted --infile=pyproject.toml --key=tool --outfile=pyproject.toml
	conda run -n works python -m toml_sorted --infile=pyproject.toml --key=tool --key=mypy --outfile=pyproject.toml

beautify: isort black jacobus toml_sorted

commit: works
	git add -A;
	conda run -n works pip install 'toml_get>=1.0,<2';
	git commit --allow-empty -m "$$(conda run -n works python -m toml_get --infile=pyproject.toml --key=project --key=version --default=unknown '--outstring=Version %s')";

clean:
	rm -fr dist/

build: works
	conda run -n works pip install 'build>=1.3,<2';
	conda run -n works python -m build;

upload: works
	conda run -n works pip install 'twine>=5.2,<7';
	conda run -n works twine upload 'dist/*';

pypi: clean build upload

test:
	@conda env remove -y -n test311 2>/dev/null || true
	conda create -y -n test311 python=3.11
	conda run -n test311 pip install -e .;
	conda run -n test311 python -c 'import toml_sorted.tests; toml_sorted.tests.test()';
	conda run -n test311 pip install mypy;
	conda run -n test311 python -m mypy -p toml_sorted;

version: beautify commit pypi
