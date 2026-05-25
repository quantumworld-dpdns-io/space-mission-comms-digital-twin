.PHONY: test build clean

test:
	cd SpaceCommsTwin && julia --project -e 'using Pkg; Pkg.test()'

build:
	cd SpaceCommsTwin && julia --project -e 'using Pkg; Pkg.add(["PyCall", "QuantumOptics", "Optim", "Plots"])'

clean:
	rm -rf SpaceCommsTwin/Manifest.toml SpaceCommsTwin/LocalPreferences.toml
