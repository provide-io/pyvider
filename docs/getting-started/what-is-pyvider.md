# 🐍 What is Pyvider?

**Pyvider** is a Python framework for building Terraform providers. It implements the Terraform Plugin Protocol v6, allowing you to create custom Terraform providers using pure Python.

## 🎯 What Problem Does It Solve?

Traditionally, Terraform providers must be written in Go. This creates barriers for teams and individuals who:

- **Prefer Python** over Go
- **Already have Python expertise** in-house
- **Want to leverage Python's ecosystem** (thousands of libraries for APIs, databases, cloud services)
- **Need rapid prototyping** without learning a new language
- **Have existing Python infrastructure code** they want to wrap as Terraform providers

Pyvider removes these barriers by letting you write providers in Python while maintaining full Terraform compatibility.

## 🤔 Who Should Use Pyvider?

### Perfect For:
- **Python developers** wanting to create custom Terraform providers
- **DevOps/Platform engineers** automating internal infrastructure
- **Teams** with existing Python codebases to expose via Terraform
- **Educators** teaching infrastructure-as-code concepts
- **Rapid prototyping** of provider ideas before committing to Go

### Not Ideal For:
- Public, high-traffic providers (Go may be more performant)
- Teams already proficient in Go with existing Go provider codebases
- Extremely latency-sensitive operations (though Pyvider is quite fast)

## 🚀 Key Features

- **Pure Python**: Write providers using familiar Python patterns
- **Protocol v6**: Latest Terraform plugin protocol
- **Async by default**: Built on modern async/await Python
- **Type-safe**: Leverages Python type hints and attrs
- **Decorator-based**: Simple registration system
- **Well-tested**: Comprehensive test suite

## ⚠️ Current Status

**Pyvider is in alpha (v0.0.x)**:
- APIs may change before 1.0
- Best suited for internal tooling and experimentation
- Not yet recommended for public providers
- Active development toward 1.0 release

See the [Roadmap](../development/roadmap.md) for future plans.
