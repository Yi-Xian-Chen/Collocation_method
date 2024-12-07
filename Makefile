clean:
	rm -rf build dist *.egg-info

uninstall:
	pip3 uninstall -y Collocation

install: clean uninstall
	python3 -m build
	pip3 install dist/*.whl

