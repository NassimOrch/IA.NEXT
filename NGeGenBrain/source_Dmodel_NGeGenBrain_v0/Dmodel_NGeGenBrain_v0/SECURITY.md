# Security policy

NGeGenBrain_v0 is intended to run locally. The built-in HTTP server binds to loopback only and is not designed for direct exposure to the public Internet. Do not forward port 8765 from a router or place this service behind a public proxy without a separate security review and authentication/authorization layer.

Report security issues privately to the person/entity maintaining your copy; do not publish live databases, credentials, or private trace data. The packaged code has no external service or package installation requirement. User-supplied programs are declarative JSON ASTs and are not passed to Python `eval` or `exec`. The security claim is specific to the implementation and tests; it is not a statement that all possible vulnerabilities are absent.

Before a public release, identify the rights holder for the custom non-commercial license and review legal and security obligations for the intended jurisdiction.
