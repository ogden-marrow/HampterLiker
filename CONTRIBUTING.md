# 🤝 Contributing to HampterLiker

Thank you for your interest in contributing to HampterLiker! 🐹

## 🌟 How to Contribute

### Reporting Bugs 🐛

If you find a bug, please open an issue with:
- A clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Your Python version and OS
- Screenshots if applicable

### Suggesting Features 💡

We love new ideas! Open an issue with:
- A clear description of the feature
- Why it would be useful
- How it might work

### Code Contributions 💻

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Follow our coding standards:**
   - Use functional programming principles
   - Add type hints to all functions
   - Write comprehensive docstrings
   - Keep functions pure when possible
   - Use immutable data structures (dataclasses with `frozen=True`)

4. **Test your changes**
   - Make sure the GUI works
   - Test with different YouTube channels
   - Check error handling

5. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

7. **Open a Pull Request**
   - Describe what you changed and why
   - Reference any related issues

## 📝 Code Style

### Python Code Style
- Follow PEP 8
- Use type hints everywhere
- Write docstrings for all functions (Google style)
- Keep functions small and focused
- Prefer functional programming patterns

### Example:
```python
def clean_handle(handle: str) -> str:
    """
    Remove @ symbol from handle.

    Args:
        handle: Channel handle with or without @

    Returns:
        Clean handle without @
    """
    return handle.lstrip('@')
```

## 🎯 Areas for Contribution

### High Priority
- [ ] Add unit tests
- [ ] Improve error messages
- [ ] Add support for playlists
- [ ] Add option to unlike videos
- [ ] Better logging

### Nice to Have
- [ ] Dark mode for GUI
- [ ] Multiple channel support
- [ ] Export liked videos list
- [ ] Statistics dashboard
- [ ] Video filtering options

## 🚫 What We Don't Accept

- Code that bypasses YouTube's rate limits
- Features that violate YouTube's Terms of Service
- Code without type hints or docstrings
- Malicious or harmful code

## 📜 Code of Conduct

- Be respectful and kind
- Help others learn
- Focus on constructive feedback
- Remember: we're all here for the hampter! 🐹

## 🎉 Recognition

Contributors will be added to the README! Every contribution counts, no matter how small.

## 💬 Questions?

Feel free to open an issue with the "question" label. We're happy to help!

---

**Made with 💕 for the Hampter community**
