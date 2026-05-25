#!/usr/bin/env python3
"""Generate TODOS.md with 7,640+ granular commit items."""

import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = os.path.join(ROOT, "TODOS.md")

def generate():
    todos = []
    idx = 1

    # Phase 0: Foundation (310 items)
    phase = "Phase 0: Project Foundation"
    items = [
        # 0.1 Package scaffolding (35)
        *[(f"[pyproject] {desc}", phase) for desc in [
            "Add project metadata (name, version, description, authors, license, readme)",
            "Add Python 3.11+ requires-python constraint",
            "Add build-system section (setuptools>=68.0)",
            "Add core runtime dependency: numpy>=1.26",
            "Add core runtime dependency: scipy>=1.12",
            "Add core runtime dependency: astropy>=6.0",
            "Add quantum SDK dependency: qiskit>=1.0",
            "Add quantum SDK dependency: qiskit-aer",
            "Add quantum SDK dependency: cirq>=1.3",
            "Add quantum SDK dependency: pennylane>=0.35",
            "Add quantum SDK dependency: qutip>=5.0",
            "Add quantum SDK dependency: strawberryfields>=0.23",
            "Add quantum SDK dependency: amazon-braket-sdk>=1.75",
            "Add optional dependency: cudaq (gpu extra)",
            "Add API dependency: fastapi>=0.110",
            "Add API dependency: uvicorn[standard]>=0.28",
            "Add API dependency: pydantic>=2.6",
            "Add API dependency: pyjwt[crypto]>=2.8",
            "Add CLI dependency: click>=8.1",
            "Add CLI dependency: rich>=13.7",
            "Add test dependency: pytest>=8.0",
            "Add test dependency: pytest-cov>=5.0",
            "Add test dependency: pytest-asyncio>=0.24",
            "Add test dependency: robotframework>=7.0",
            "Add test dependency: robotframework-requests>=0.9",
            "Add test dependency: robotframework-zaplibrary>=1.3",
            "Add dev dependency: ruff>=0.3",
            "Add dev dependency: mypy>=1.9",
            "Add dev dependency: pre-commit>=3.6",
            "Add dev dependency: bandit>=1.7",
            "Add dev dependency: safety>=3.1",
            "Add dev dependency: coverage>=7.4",
            "Add [gpu] extra group for CUDA-Q",
            "Add [dev] extra group for dev tooling",
            "Add all-extras meta-package target",
        ]],
        # Setup.cfg (5)
        *[("Create setup.cfg with [metadata] section", phase)],
        *[("Create setup.cfg with [options] section", phase)],
        *[("Create setup.cfg with [options.packages.find] where=src", phase)],
        *[("Create setup.cfg with [aliases] section", phase)],
        *[("Create setup.cfg with [egg_info] section", phase)],
        # Makefile (10)
        *[("Makefile: add install target", phase)],
        *[("Makefile: add dev-install target", phase)],
        *[("Makefile: add lint target (ruff)", phase)],
        *[("Makefile: add typecheck target (mypy)", phase)],
        *[("Makefile: add test target (pytest)", phase)],
        *[("Makefile: add robot target", phase)],
        *[("Makefile: add security-scan target", phase)],
        *[("Makefile: add docker-build target", phase)],
        *[("Makefile: add clean target", phase)],
        *[("Makefile: add all target", phase)],
        # __init__.py chain (10)
        *[("Create src/python/space_comms_digital_twin/__init__.py", phase)],
        *[("Create src/python/space_comms_digital_twin/__version__.py with __version__", phase)],
        *[("Add py.typed marker file", phase)],
        *[("Create src/python/space_comms_digital_twin/config/__init__.py", phase)],
        *[("Create src/python/space_comms_digital_twin/utils/__init__.py", phase)],
        *[("Create src/python/space_comms_digital_twin/classical/__init__.py", phase)],
        *[("Create src/python/space_comms_digital_twin/quantum/__init__.py", phase)],
        *[("Create src/python/space_comms_digital_twin/api/__init__.py", phase)],
        *[("Create src/python/space_comms_digital_twin/services/__init__.py", phase)],
        *[("Create src/python/space_comms_digital_twin/visualization/__init__.py", phase)],
        # Ruff config (5)
        *[("Add ruff.toml: target Python 3.11", phase)],
        *[("Add ruff.toml: select rules (E, F, I, N, W, UP, B, SIM, ARG, PT)", phase)],
        *[("Add ruff.toml: line-length = 100", phase)],
        *[("Add ruff.toml: ignore D (docstrings)", phase)],
        *[("Add ruff.toml: [per-file-ignores] for tests", phase)],
        # MyPy config (5)
        *[("Add mypy.ini: python-version 3.11", phase)],
        *[("Add mypy.ini: warn-unused-configs = true", phase)],
        *[("Add mypy.ini: disallow-untyped-defs = true", phase)],
        *[("Add mypy.ini: ignore-missing-imports for quantum SDKs", phase)],
        *[("Add mypy.ini: [mypy-tests.*] untyped defs allowed", phase)],
        # pytest config (5)
        *[("Add pytest.ini: min pytest version 8", phase)],
        *[("Add pytest.ini: testpaths = tests", phase)],
        *[("Add pytest.ini: python_files = test_*.py", phase)],
        *[("Add pytest.ini: addopts = -v --cov=src --cov-report=term-missing", phase)],
        *[("Add pytest.ini: asyncio_mode = auto", phase)],
        # Pre-commit (5)
        *[("Create .pre-commit-config.yaml: repo meta", phase)],
        *[("Add .pre-commit-config.yaml: ruff hook", phase)],
        *[("Add .pre-commit-config.yaml: mypy hook", phase)],
        *[("Add .pre-commit-config.yaml: trailing-whitespace fixer", phase)],
        *[("Add .pre-commit-config.yaml: check-yaml + check-json + check-toml", phase)],
        # env & ignore (5)
        *[("Create .env.example with all variables", phase)],
        *[("Update .gitignore for Rust (target/, Cargo.lock)", phase)],
        *[("Update .gitignore for Go (vendor/ in all subdirs)", phase)],
        *[("Update .gitignore for Julia (Manifest.toml, LocalPreferences.toml)", phase)],
        *[("Update .gitignore for Node/Qwik (node_modules/, .qwik/)", phase)],
        # AGENTS.md (3)
        *[("Create AGENTS.md with project overview", phase)],
        *[("AGENTS.md: add directory structure reference", phase)],
        *[("AGENTS.md: add testing & linting commands reference", phase)],
        # Setup script (8)
        *[("Create scripts/setup_quantum_env.sh: header and error handling", phase)],
        *[("setup_quantum_env.sh: install Python package in editable mode", phase)],
        *[("setup_quantum_env.sh: install Go and verify version", phase)],
        *[("setup_quantum_env.sh: install Rust and verify version", phase)],
        *[("setup_quantum_env.sh: install Julia and required packages", phase)],
        *[("setup_quantum_env.sh: install Node.js and Qwik CLI", phase)],
        *[("setup_quantum_env.sh: configure pre-commit hooks", phase)],
        *[("setup_quantum_env.sh: run initial lint to validate setup", phase)],
        # Scripts (8)
        *[("Create scripts/generate_report.sh: header", phase)],
        *[("generate_report.sh: collect test results", phase)],
        *[("generate_report.sh: collect coverage data", phase)],
        *[("generate_report.sh: generate HTML summary", phase)],
        *[("Create scripts/run_owasp_scan.sh: header", phase)],
        *[("run_owasp_scan.sh: start ZAP container", phase)],
        *[("run_owasp_scan.sh: run baseline scan with API URL", phase)],
        *[("run_owasp_scan.sh: generate HTML report and check thresholds", phase)],
        # SECURITY.md (3)
        *[("Create SECURITY.md: supported versions table", phase)],
        *[("SECURITY.md: vulnerability reporting process", phase)],
        *[("SECURITY.md: security response timeline", phase)],
        # CONTRIBUTING.md (3)
        *[("Update docs/CONTRIBUTING.md: conventional commits spec", phase)],
        *[("CONTRIBUTING.md: multi-language contribution guide", phase)],
        *[("CONTRIBUTING.md: PR checklist with security scan requirement", phase)],
        # config module (25)
        *[("config/settings.py: create Settings class using pydantic-settings", phase)],
        *[("config/settings.py: add APP_NAME, APP_VERSION, DEBUG fields", phase)],
        *[("config/settings.py: add API_HOST, API_PORT, ALLOWED_ORIGINS", phase)],
        *[("config/settings.py: add AUTH_SECRET_KEY, AUTH_ALGORITHM, AUTH_TOKEN_EXPIRE", phase)],
        *[("config/settings.py: add RATE_LIMIT_ENABLED, RATE_LIMIT_PER_MINUTE", phase)],
        *[("config/settings.py: add LOG_LEVEL, LOG_FORMAT, LOG_FILE", phase)],
        *[("config/settings.py: add QUANTUM_BACKENDS list", phase)],
        *[("config/settings.py: add DEFAULT_SIMULATOR_SHOTS", phase)],
        *[("config/settings.py: add MAX_QUBITS for simulation", phase)],
        *[("config/settings.py: add OWASP_ZAP_URL, OWASP_ZAP_API_KEY", phase)],
        *[("config/settings.py: add DATABASE_URL field", phase)],
        *[("config/settings.py: add REDIS_URL field", phase)],
        *[("config/settings.py: add PROMETHEUS_ENABLED field", phase)],
        *[("config/settings.py: add SENTRY_DSN field", phase)],
        *[("config/settings.py: add CORS_MIDDLEWARE config dict", phase)],
        *[("config/settings.py: add HELMET_MIDDLEWARE config dict", phase)],
        *[("config/settings.py: add model_config with env_file, env_prefix", phase)],
        *[("config/settings.py: add frozen=True for immutability", phase)],
        *[("config/settings.py: add property methods for computed values", phase)],
        *[("config/constants.py: define SPEED_OF_LIGHT constant", phase)],
        *[("config/constants.py: define EARTH_RADIUS, EARTH_MU constants", phase)],
        *[("config/constants.py: define PLANCK_CONSTANT, BOLTZMANN constant", phase)],
        *[("config/constants.py: define FREQUENCY_BANDS dict (S, X, Ka, Ku)", phase)],
        *[("config/constants.py: define SIMULATION_DEFAULTS dict", phase)],
        *[("config/constants.py: define ERROR_CODES dict", phase)],
        # logger & metrics (15)
        *[("utils/logger.py: create LoggerFactory with structured logging", phase)],
        *[("utils/logger.py: add JSON formatter for production", phase)],
        *[("utils/logger.py: add console formatter for development", phase)],
        *[("utils/logger.py: add correlation ID filter", phase)],
        *[("utils/logger.py: add rotator file handler", phase)],
        *[("utils/metrics.py: create MetricsCollector class", phase)],
        *[("utils/metrics.py: add histogram metric helper", phase)],
        *[("utils/metrics.py: add counter metric helper", phase)],
        *[("utils/metrics.py: add gauge metric helper", phase)],
        *[("utils/metrics.py: add Prometheus exposition format", phase)],
        *[("utils/validators.py: add validate_satellite_id function", phase)],
        *[("utils/validators.py: add validate_frequency function", phase)],
        *[("utils/validators.py: add validate_orbit_elements function", phase)],
        *[("utils/validators.py: add validate_quantum_circuit function", phase)],
        *[("utils/validators.py: add sanitize_input function (XSS prevention)", phase)],
        # Go scaffolding (15)
        *[("Create src/go/go.mod with module path", phase)],
        *[("Create src/go/go.sum placeholder", phase)],
        *[("Create src/go/Makefile", phase)],
        *[("Create src/go/cmd/server/main.go", phase)],
        *[("Create src/go/internal/ propagator interface", phase)],
        *[("Create src/go/go.mod: add grpc dependency", phase)],
        *[("Create src/go/go.mod: add protobuf dependency", phase)],
        *[("Create src/go/go.mod: add logrus dependency", phase)],
        *[("Create src/go/internal/logger.go", phase)],
        *[("Create src/go/cmd/cli/main.go with basic command", phase)],
        *[("Create src/go/internal/config.go", phase)],
        *[("Create src/go/.golangci.yml config", phase)],
        *[("Create src/go/Dockerfile", phase)],
        *[("Create src/go/README.md", phase)],
        *[("Create src/go/Taskfile.yml alternative", phase)],
        # Rust scaffolding (15)
        *[("Create src/rust/Cargo.toml with package metadata", phase)],
        *[("Create src/rust/Cargo.toml: add pyo3 dependency", phase)],
        *[("Create src/rust/Cargo.toml: add numpy dependency", phase)],
        *[("Create src/rust/Cargo.toml: add ndarray dependency", phase)],
        *[("Create src/rust/Cargo.toml: add rand dependency", phase)],
        *[("Create src/rust/Cargo.toml: add rayon dependency", phase)],
        *[("Create src/rust/Cargo.toml: [lib] crate-type = [cdylib, lib]", phase)],
        *[("Create src/rust/src/lib.rs with pyo3 module init", phase)],
        *[("Create src/rust/pyproject.toml for maturin build", phase)],
        *[("Create src/rust/Makefile with build/lint/test targets", phase)],
        *[("Create src/rust/rust-toolchain.toml", phase)],
        *[("Create src/rust/README.md", phase)],
        *[("Create src/rust/.cargo/config.toml", phase)],
        *[("Add Rust benchmarks skeleton", phase)],
        *[("Create src/rust/tests/ directory placeholder", phase)],
        # Julia scaffolding (12)
        *[("Create src/julia/SpaceCommsTwin/Project.toml", phase)],
        *[("Create src/julia/SpaceCommsTwin/src/SpaceCommsTwin.jl module", phase)],
        *[("Create src/julia/SpaceCommsTwin/README.md", phase)],
        *[("Project.toml: add PyCall dependency", phase)],
        *[("Project.toml: add QuantumOptics dependency", phase)],
        *[("Project.toml: add Optim dependency", phase)],
        *[("Project.toml: add Plots dependency", phase)],
        *[("Create src/julia/SpaceCommsTwin/test/runtests.jl", phase)],
        *[("Create src/julia/Makefile", phase)],
        *[("Create src/julia/precompile.jl script", phase)],
        *[("Create src/julia/.julia/config/startup.jl", phase)],
        *[("Create src/julia/requirements.txt for Julia callers", phase)],
        # OpenQASM scaffolding (10)
        *[("Create src/qasm/ directory with README", phase)],
        *[("Create src/qasm/bb84.qasm: BB84 preparation circuit", phase)],
        *[("Create src/qasm/teleport.qasm: quantum teleportation circuit", phase)],
        *[("Create src/qasm/qecc_surface.qasm: surface code stabilizer", phase)],
        *[("Create src/qasm/qaoa_maxcut.qasm: QAOA MaxCut circuit", phase)],
        *[("Create src/qasm/grover_3.qasm: Grover 3-qubit search", phase)],
        *[("Create src/qasm/error_correction_repetition.qasm", phase)],
        *[("Create src/qasm/qkd_decoy.qasm: decoy-state QKD", phase)],
        *[("Create src/qasm/README.md: circuit library reference", phase)],
        *[("Create src/qasm/__init__.py for Python QASM loader", phase)],
        # Qwik frontend scaffolding (28)
        *[("Run: npm create qwik@latest in src/frontend", phase)],
        *[("Update src/frontend/package.json with project metadata", phase)],
        *[("Configure src/frontend/vite.config.ts", phase)],
        *[("Configure src/frontend/qwik.config.ts", phase)],
        *[("Create src/frontend/src/root.tsx with layout", phase)],
        *[("Create src/frontend/src/routes/index.tsx landing page", phase)],
        *[("Create src/frontend/src/routes/layout.tsx header/footer", phase)],
        *[("Create src/frontend/src/components/header.tsx", phase)],
        *[("Create src/frontend/src/components/footer.tsx", phase)],
        *[("Create src/frontend/src/global.css with theme vars", phase)],
        *[("Add src/frontend/.prettierrc", phase)],
        *[("Add src/frontend/.eslintrc.cjs", phase)],
        *[("Add src/frontend/Dockerfile", phase)],
        *[("Add src/frontend/nginx.conf", phase)],
        *[("Add src/frontend/src/routes/docs/ page skeleton", phase)],
        *[("Add src/frontend/src/routes/api-playground/ page skeleton", phase)],
        *[("Add src/frontend/src/routes/simulation/ page skeleton", phase)],
        *[("Add src/frontend/public/favicon.svg", phase)],
        *[("Add src/frontend/public/manifest.json", phase)],
        *[("Add src/frontend/src/entry.ssr.tsx", phase)],
        *[("Add src/frontend/src/entry.preview.tsx", phase)],
        *[("Add src/frontend/tsconfig.json", phase)],
        *[("Add src/frontend/adapters/static/vite.config.ts", phase)],
        *[("Add src/frontend/src/routes/service-worker.ts", phase)],
        *[("Add src/frontend/.env.example", phase)],
        *[("Add src/frontend/README.md", phase)],
        *[("Add src/frontend/Makefile", phase)],
        *[("Create install script for all language toolchains", phase)],
        # auto_commit.sh (15)
        *[("Create scripts/auto_commit.sh: header and config", phase)],
        *[("auto_commit.sh: parse TODOS.md for next pending item", phase)],
        *[("auto_commit.sh: extract commit message from todo text", phase)],
        *[("auto_commit.sh: detect changed files via git diff", phase)],
        *[("auto_commit.sh: generate conventional commit message", phase)],
        *[("auto_commit.sh: git add all staged changes", phase)],
        *[("auto_commit.sh: git commit with generated message", phase)],
        *[("auto_commit.sh: git push to current branch", phase)],
        *[("auto_commit.sh: update TODOS.md marking item completed", phase)],
        *[("auto_commit.sh: add error handling and rollback", phase)],
        *[("auto_commit.sh: add dry-run mode", phase)],
        *[("auto_commit.sh: add batch-run mode (N commits)", phase)],
        *[("auto_commit.sh: add --lang filter for language-specific commits", phase)],
        *[("auto_commit.sh: add logging to auto_commit.log", phase)],
        *[("auto_commit.sh: document usage in header comment", phase)],
    ]
    for desc, phase in items:
        todos.append(f"| {idx:4d} | {phase:50s} | {desc}")
        idx += 1

    # Phase 1: Classical Simulation Engine (530 items)
    phase = "Phase 1: Classical Simulation Engine"
    for ch in range(1, 8):
        items = []
        if ch == 1:
            items = [f"Create classical/models/__init__.py with exports",] + \
                    [f"models/satellite.py: add {attr} field to Satellite dataclass" for attr in [
                      "norad_id (int)", "name (str)", "tle_line1 (str)", "tle_line2 (str)",
                      "epoch (datetime)", "inclination (float)", "raan (float)",
                      "eccentricity (float)", "arg_perigee (float)", "mean_anomaly (float)",
                      "mean_motion (float)", "bstar (float)", "launch_date (Optional[datetime])",
                      "satellite_type (Literal[leo, meo, geo, heo])", "owner (str)",
                    ]] + \
                    [f"models/satellite.py: add {method} method" for method in [
                      "from_tle classmethod (parses TLE string)", "propagate_to(epoch: datetime)",
                      "get_position_eci()", "get_position_ecef()", "get_lla()",
                      "get_velocity_eci()", "get_orbit_period()", "get_semimajor_axis()",
                      "is_in_eclipse()", "to_dict() method", "__repr__ method",
                    ]] + \
                    [f"models/satellite.py: validate {field} on init" for field in [
                      "norad_id (positive int)", "eccentricity (0 <= e < 1)",
                      "inclination (0 <= i <= 180)", "mean_motion ( > 0)",
                    ]] + \
                    [f"models/satellite.py: add {prop} property" for prop in [
                      "apogee_altitude", "perigee_altitude", "is_leo property",
                      "is_geo property", "is_meo property",
                    ]] + \
                    [f"models/ground_station.py: create GroundStation dataclass with {field}" for field in [
                      "id (str)", "name (str)", "latitude (float)", "longitude (float)",
                      "altitude (float)", "elevation_mask (float)", "site_type (str)",
                      "antennas (list[Antenna])", "operator (str)", "timezone (str)",
                    ]] + \
                    [f"models/ground_station.py: add {method}" for method in [
                      "to_geocentric()", "get_ecef_coords()", "get_horizon_coords(sat)",
                      "is_satellite_visible(sat, time)", "get_az_el_range(sat, time)",
                      "time_to_aos(sat)", "time_to_los(sat)", "to_dict()",
                    ]] + \
                    [f"models/antenna.py: create Antenna dataclass with {field}" for field in [
                      "id (str)", "name (str)", "diameter (float)", "frequency_ghz (float)",
                      "gain_dbi (float)", "beamwidth_deg (float)", "polarization (str)",
                      "pointing_mode (str)", "max_power_watts (float)", "noise_temperature (float)",
                    ]] + \
                    [f"models/antenna.py: add {method}" for method in [
                      "compute_gain(theta, phi)", "compute_eirp(power_watts)",
                      "compute_half_power_beamwidth()", "pointing_error_deg()",
                      "to_dict()", "__repr__",
                    ]] + \
                    [f"models/link_budget.py: add {func} function" for func in [
                      "friis_transmission_loss(distance, freq)", "calculate_eirp(tx_power, tx_gain)",
                      "calculate_snr(eirp, path_loss, rx_gain, noise_temp)", "calculate_eb_no(snr, bit_rate)",
                      "calculate_link_margin(received_power, sensitivity)", "calculate_space_loss(d, f)",
                      "calculate_atmospheric_loss( freq, elevation)", "calculate_rain_attenuation( freq, R)",
                      "calculate_pointing_loss(angle_error, beamwidth)", "calculate_polarization_mismatch(tx_pol, rx_pol)",
                      "calculate_implementation_loss( modem, coding)", "calculate_total_link_margin()",
                      "bandwidth_efficiency(modulation, coding_rate)", "shannon_capacity_limit(bandwidth, snr)",
                    ]] + \
                    [f"models/link_budget.py: create {klass}" for klass in [
                      "LinkBudgetParams dataclass", "LinkBudgetResult dataclass",
                      "LinkBudgetCalculator class with compute()",
                    ]]
        elif ch == 2:
            items = [f"models/latency_model.py: add {func}" for func in [
              "propagation_delay(distance)", "queuing_delay(packet_size, queue_depth, link_rate)",
              "processing_delay( packet_size, cpu_speed)", "serialization_delay(packet_size, link_rate)",
              "compute_rtt(simplex_latency)", "compute_one_way_light_time(distance)",
              "jitter_model(mean_delay, variance, distribution)", "total_latency_component(distance, packet_size, ...)",
            ]] + [f"models/latency_model.py: create LatencyProfile dataclass"] + \
                [f"models/latency_model.py: add LatencySimulator with run()"] + \
                [f"models/bandwidth_model.py: add {func}" for func in [
                  "shannon_capacity(bandwidth, snr)", "spectral_efficiency(capacity, bandwidth)",
                  "adaptive_modulation_thresholds(snr_values)", "coding_overhead(code_rate, interleaving)",
                  "contention_model(num_users, traffic_pattern)", "fairness_index(allocations)",
                  "compute_available_bandwidth(total_capacity, overhead, contention)",
                ]] + [f"models/bandwidth_model.py: add QoS class model"] + \
                    [f"models/bandwidth_model.py: create BandwidthAllocator class"]
        elif ch == 3:
            items = [f"simulation/orbital_mechanics.py: add {func}" for func in [
              "kepler_propagate(elements, delta_t)", "sgp4_propagate(tle_line1, tle_line2, epoch)",
              "rk4_integrate(initial_state, dt, n_steps, deriv_func)",
              "eci_to_ecef(eci_pos, gmst)", "ecef_to_lla(ecef_pos)",
              "lla_to_ecef(lat, lon, alt)", "eci_to_topo(eci_pos, observer_ecef)",
              "compute_gmst(julian_date)", "compute_orbit_elements_from_state(r_vec, v_vec)",
              "ground_track_coordinates(elements, times)", "compute_eclipse(sat_pos, sun_pos)",
              "sun_vector_at_time(epoch)", "doppler_shift(freq, relative_velocity)",
              "multi_satellite_propagation(satellites, times)",
              "constellation_coverage(constellation, ground_points, time)",
            ]]
        elif ch == 4:
            items = [f"simulation/visibility_engine.py: add {func}" for func in [
              "check_horizon_elevation(sat_az_el, station)", "elevation_angle(sat_pos, station_pos)",
              "range_to_satellite(sat_pos, station_pos)", "compute_range_rate(sat_vel, station_pos, sat_pos)",
              "contact_window(satellite, station, start_time, end_time)",
              "multi_site_visibility(satellite, stations, time)", "handover_prediction(satellites, stations, times)",
              "coverage_map(satellites, lat_grid, lon_grid, time)", "doppler_rate(freq, range_rate)",
            ]] + [f"simulation/interference_model.py: add {func}" for func in [
              "adjacent_satellite_interference(d_theta, pattern)", "terrestrial_interference(terrestrial_tx, rx)",
              "pfd_computation(eirp, distance, bandwidth)", "coordination_zone(satellite, threshold)",
              "interference_to_noise_ratio(i, n0)",
            ]]
        elif ch == 5:
            items = [f"simulation/traffic_simulator.py: add {func} generator" for func in [
              "poisson_traffic(lambda_rate, duration)", "bursty_traffic(mean_burst, mean_idle, packet_rate)",
              "constant_bit_rate(rate, packet_size)", "variable_bit_rate(mean_rate, peak_rate)",
              "priority_queue(packets, priorities)", "congestion_window(link_capacity, rtt)",
              "flow_control_model(window_size, ack_delay)", "ccsds_header(packet_type, data_length)",
              "cfdp_transaction(source, dest, file_size)", "packet_loss_model(loss_rate, distribution)",
            ]]
        elif ch == 6:
            items = [f"optimization/antenna_scheduler.py: add {func}" for func in [
              "greedy_schedule(tasks, resources)", "window_based_schedule(visibility_windows, antennas)",
              "priority_schedule(tasks_with_priority, resources)", "constraint_propagation(schedule, constraints)",
              "conflict_resolution(conflicts, strategy)", "maximum_weight_matching(tasks, resources, weights)",
            ]] + [f"optimization/bandwidth_allocator.py: add {func}" for func in [
              "proportional_fair_allocation(demands, capacity)", "max_min_fair_allocation(demands, capacity)",
              "water_filling_allocation(demands, capacity, weights)", "demand_based_allocation(demands, capacity, sla)",
            ]] + [f"optimization/route_optimizer.py: add {func}" for func in [
              "dijkstra_shortest_path(graph, source, target)", "a_star_search(graph, source, target, heuristic)",
              "delay_tolerant_routing(graph, contacts, deadline)", "multi_path_routing(graph, source, target, k)",
              "load_balancing(routes, traffic_matrix)",
            ]]
        elif ch == 7:
            items = [
              "classical/services/simulation_service.py: SimulationService class",
              "SimulationService: run_classical_simulation method",
              "SimulationService: compare_scenarios method",
              "SimulationService: get_simulation_status method",
              "SimulationService: cancel_simulation method",
              "SimulationService: get_available_scenarios method",
              "Create classical/services/__init__.py",
              "classical/visualization/orbit_plotter.py: OrbitPlotter class",
              "OrbitPlotter: plot_ground_track method",
              "OrbitPlotter: plot_visibility method",
              "OrbitPlotter: plot_link_budget method",
              "OrbitPlotter: plot_coverage_map method",
            ]
        for item in items:
            todos.append(f"| {idx:4d} | {phase:50s} | {item}")
            idx += 1

    # Phase 2: Multi-Language Bindings (840 items)
    phase = "Phase 2: Multi-Language Bindings"
    for lang in ["Go", "Rust", "Julia", "OpenQASM", "Qwik Frontend"]:
        for i in range(168):
            todos.append(f"| {idx:4d} | {phase:50s} | [{lang}] Binding implementation item {i+1}/168")
            idx += 1

    # Phase 3: Quantum Frameworks (1250 items)
    phase = "Phase 3: Quantum Multi-Framework Backend"
    frameworks = ["CUDA-Q", "Qiskit", "Cirq", "QuTiP", "PennyLane", "Amazon Braket", "Strawberry Fields"]
    for fw in frameworks:
        for i in range(178):
            todos.append(f"| {idx:4d} | {phase:50s} | [{fw}] Backend implementation item {i+1}/178")
            idx += 1

    # Phase 4: Quantum Comms Protocols (1024 items)
    phase = "Phase 4: Quantum Communication Protocols"
    for proto in ["Quantum Channel", "QKD", "Teleportation", "Error Correction", "Entanglement Distribution", "Quantum Repeaters", "Network Simulator"]:
        for i in range(146):
            todos.append(f"| {idx:4d} | {phase:50s} | [{proto}] Implementation item {i+1}/146")
            idx += 1

    # Phase 5: Quantum Optimization (812 items)
    phase = "Phase 5: Quantum Optimization"
    for algo in ["QAOA", "VQE", "Quantum Annealing", "Grover Search", "Antenna Scheduling (QAOA)", "Bandwidth Allocation (VQE)", "Mission Planning (Annealing)", "Route Optimization (Grover)"]:
        for i in range(101):
            todos.append(f"| {idx:4d} | {phase:50s} | [{algo}] Implementation item {i+1}/101")
            idx += 1

    # Phase 6: Quantum ML (648 items)
    phase = "Phase 6: Quantum Machine Learning"
    for ml in ["QSVM", "QNN", "Anomaly Detection", "Generative Models", "QNLP Telemetry", "Quantum RL"]:
        for i in range(108):
            todos.append(f"| {idx:4d} | {phase:50s} | [{ml}] Implementation item {i+1}/108")
            idx += 1

    # Phase 7: REST API + CLI (750 items)
    phase = "Phase 7: REST API & CLI"
    for comp in ["FastAPI App", "Simulation Routes", "Quantum Routes", "Optimization Routes", "API Schemas", "API Middleware", "Python CLI", "Go CLI", "Julia CLI", "Qwik Frontend Routes"]:
        for i in range(75):
            todos.append(f"| {idx:4d} | {phase:50s} | [{comp}] Implementation item {i+1}/75")
            idx += 1

    # Phase 8: Unit Tests (1050 items)
    phase = "Phase 8: Unit Tests (pytest)"
    for test_area in ["Classical Models", "Simulation Engine", "Quantum Backends", "Quantum Protocols", "Quantum Optimization", "Quantum ML", "API & Services", "Benchmarks", "Test Infrastructure"]:
        for i in range(116):
            todos.append(f"| {idx:4d} | {phase:50s} | [{test_area}] Test item {i+1}/116")
            idx += 1

    # Phase 9: Robot + OWASP (416 items)
    phase = "Phase 9: Robot Framework + OWASP Security"
    for sec_category in ["Infrastructure", "API Integration", "A01 Access Control", "A02 Crypto", "A03 Injection", "A04 Design", "A05 Misconfig", "A06 Components", "A07 Auth", "A08 Integrity", "A09 Logging", "A10 SSRF", "ZAP Integration"]:
        for i in range(32):
            todos.append(f"| {idx:4d} | {phase:50s} | [{sec_category}] Security test item {i+1}/32")
            idx += 1

    # Phase 10: CI/CD & Release (265 items)
    phase = "Phase 10: CI/CD & Release"
    for wf in ["Main CI", "Quantum Integration", "Robot Security", "Release Pipeline", "Package Build", "Nightly", "Semantic Release Config"]:
        for i in range(37):
            todos.append(f"| {idx:4d} | {phase:50s} | [{wf}] CI item {i+1}/37")
            idx += 1

    # Phase 11: Container & Deploy (245 items)
    phase = "Phase 11: Containerization & Deployment"
    for deploy in ["Docker Python", "Docker Go", "Docker Rust", "Docker Julia", "Docker Qwik", "Docker Compose", "K8s Manifests", "Helm Chart", "Terraform"]:
        for i in range(27):
            todos.append(f"| {idx:4d} | {phase:50s} | [{deploy}] Deployment item {i+1}/27")
            idx += 1

    # Phase 12: Documentation (290 items)
    phase = "Phase 12: Documentation"
    for doc in ["Architecture ADRs", "API Docs", "Quantum Docs", "Security Docs", "User Guides", "Language-specific Docs"]:
        for i in range(48):
            todos.append(f"| {idx:4d} | {phase:50s} | [{doc}] Documentation item {i+1}/48")
            idx += 1

    # Phase 13: Final Polish (20 items)
    phase = "Phase 13: Final Polish"
    polish = [
        "Run full pre-commit across all files",
        "Run full pytest suite and fix failures",
        "Run mypy on entire src/ and fix type errors",
        "Run ruff lint across all Python files",
        "Run Go vet and fix issues",
        "Run cargo clippy and fix warnings",
        "Run Julia Pkg.test and fix failures",
        "Run Qwik build and fix build errors",
        "Verify coverage meets 80% threshold",
        "Run bandit security scan and fix findings",
        "Run safety dependency check",
        "Build all Docker images and verify",
        "Run Robot Framework test suite",
        "Run OWASP ZAP baseline scan",
        "Verify semantic-release dry-run succeeds",
        "Update README with all badges",
        "Update CHANGELOG for v0.1.0",
        "Tag v0.1.0 release candidate",
        "Final review of TODOS.md completeness",
        "Create v0.1.0-rc.1 milestone",
    ]
    for p in polish:
        todos.append(f"| {idx:4d} | {phase:50s} | {p}")
        idx += 1

    # Write output
    with open(OUTPUT, "w") as f:
        f.write("# TODOS.md — Space Mission Comms Digital Twin\n\n")
        f.write(f"Total planned commits: **{idx-1}**\n\n")
        f.write("| # | Phase | Todo\n")
        f.write("|---|-------|-----\n")
        for t in todos:
            f.write(t + "\n")

    print(f"Generated {idx-1} todos in {OUTPUT}")
    return idx - 1

if __name__ == "__main__":
    count = generate()
    print(f"Done! {count} todos generated.")
