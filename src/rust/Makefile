.PHONY: build test lint clean bench develop

build:
	cargo build

release:
	cargo build --release

test:
	cargo test

lint:
	cargo clippy -- -D warnings

fmt:
	cargo fmt

clean:
	cargo clean

bench:
	cargo bench

develop:
	maturin develop --release
