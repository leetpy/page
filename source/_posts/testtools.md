---
title: testtools
date: 2018-12-21 15:27:25
tags: [python]
---

testools是属于python中诸多自动化框架中的一个, 是python标准库中unittest的扩展。

<!-- more -->

## 优点

- 更好的assertion method
- 更多的调试信息
- 扩展自unittest，但是兼容unittest
- 支持不同python版本

## assertion

- assertRaises
  ```python
  def test_square_bad_input(self):
    # 'square' raises a TypeError if it's given bad input, say a
    # string.
    e = self.assertRaises(TypeError, silly.square, "orange")
    self.assertEqual("orange", e.bad_value)
    self.assertEqual("Cannot square 'orange', not a number.", str(e))
  ```
- ExpectedException
  ```python
  def test_square_root_bad_input_2(self):
    # 'square' raises a TypeError if it's given bad input.
    with ExpectedException(TypeError, "Cannot square.*"):
        silly.square('orange')
  ```
