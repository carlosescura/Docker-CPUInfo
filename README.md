# CPUinfo Docker container

Simple Docker container that exposes container's CPU info via web API

## Build the Docker image

To start the project, you just need to build the Docker image running:

```sh
make build
```

Or using optional parameters like image tag:

```sh
make build BUILD_TAG=your_name
```

Default image name is `cpu-info-test`

## Run the Docker image

Start the image running:

```sh
make run
```

or if you prefer starting the container in background:

```sh
make run-daemon
```

Optional parameters for `run` and `run-daemon` are:
`BUILD_TAG` which denotes the Docker image name/tag to use
`EXPOSED_PORT` which changes the exposed web service port, and defaults to `8080`

## Test the service

Test the service running:

```sh
curl http://localhost:8080
```

Expected output should be:

```json
{
  "arch": "X86_64",
  "bits": 64,
  "brand": "Intel(R) Core(TM) i7-7820HQ CPU @ 2.90GHz",
  "count": 4,
  "cpuinfo_version": [4, 0, 0],
  "extended_model": 9,
  "family": 6,
  "flags": [
    "hypervisor",
    "ss",
    "sse",
    "sse2",
    "sse4_1",
    "sse4_2",
    "ssse3",
    "..."
  ],
  "hz_actual": "2.9000 GHz",
  "hz_actual_raw": [2900000000, 0],
  "hz_advertised": "2.9000 GHz",
  "hz_advertised_raw": [2900000000, 0],
  "l1_data_cache_size": "32 KB",
  "l1_instruction_cache_size": "32 KB",
  "l2_cache_associativity": "0x100",
  "l2_cache_line_size": 6,
  "l2_cache_size": "256 KB",
  "l3_cache_size": "8192KB",
  "model": 158,
  "python_version": "3.7.1.final.0 (64 bit)",
  "raw_arch_string": "x86_64",
  "stepping": 9,
  "vendor_id": "GenuineIntel"
}
```
