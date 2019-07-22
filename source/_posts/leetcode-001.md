---
title: Two Sum
date: 2015-01-28 23:09:30
tags: [leetcode]
---

## 描述

Given an array of integers, return indices of the two numbers such that they add up to a specific target.
You may assume that each input would have exactly one solution, and you may not use the same element twice.

<!-- more -->

题目链接：[https://leetcode.com/problems/two-sum/description/](https://leetcode.com/problems/two-sum/description/)


## 分析

这一题最直观的思路就是两层for循环，但是这样时间复杂度是O(n^2)。 因为题目里告诉了只有唯一解，所有我们可以使用hash来做。

## 代码实现

### go实现

```go
func twoSum(nums []int, target int) []int {
    m1 := make(map[int]int)
    for index, value := range nums {
        m1[value] = index
    }
    for index, value := range nums {
        complement := target - value
        if v, ok := m1[complement]; ok {
            if m1[complement] != index {
                return []int{index, v}
            }
        }
    }
    return []int{}
}
```

### python实现

```python
class Solution(object):
    def twoSum(self, nums, target):
        result = []
        data = {}
        for i in range(len(nums)):
            if (target - nums[i]) in data.keys():
                result.append(data.get(target - nums[i])+1)
                result.append(i+1)
            else:
                data[nums[i]] = i
        return result
```



