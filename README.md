# LeetCode

> [!IMPORTANT]
> 本仓库暂停更新, 新题解请前往[博客](https://xubinh.github.io/tags/leetcode/).

刷题记录 (从上到下按刷题时间顺序从早到晚排序)

## <a id="toc"></a>目录

<details open="open"><summary><a href="#1">题目</a></summary>

- <a href="#1.1">1. 两数之和 | 简单</a>
- <a href="#1.2">2. 两数相加 | 中等</a>
- <a href="#1.3">3. 无重复字符的最长子串 | 中等</a>
- <a href="#1.4">4. 寻找两个正序数组的中位数 | 困难</a>
- <a href="#1.5">5. 最长回文子串 | 中等</a>
- <a href="#1.6">10. 正则表达式匹配 | 困难</a>
- <a href="#1.7">11. 盛最多水的容器 | 中等</a>
- <a href="#1.8">105. 从前序与中序遍历序列构造二叉树 | 中等</a>
- <a href="#1.9">26. 删除有序数组中的重复项 | 简单</a>
- <a href="#1.10">80. 删除有序数组中的重复项 II | 中等</a>
- <a href="#1.11">69. x 的平方根 | 简单</a>
- <a href="#1.12">124. 二叉树中的最大路径和 | 困难</a>
- <a href="#1.13">102. 二叉树的层序遍历 | 中等</a>
- <a href="#1.14">199. 二叉树的右视图 | 中等</a>

</details>

<div align="right"><b><a href="#toc">返回顶部↑</a></b></div>

## <a id="1"></a>题目

### <a id="1.1"></a>1. 两数之和 | 简单

问题设置: 给定一个乱序正负整数数组, 数组长度量级 1e4, 元素大小量级 1e9, 再给定一个整数 target

要求: 返回数组中两个加起来等于 target 的整数的**下标**. 两个下标不能够相同.

思路:

- 第一反应是排序 + 双指针, 但这样做会丢失下标信息, 需要在找到方案之后再拿着方案回原数组遍历一遍. 时间消耗是 $O(n \log n)$
- 第二反应是使用哈希表, 但是**当时**觉得哈希表的大小和元素大小量级正相关, 为 1e9, 太大了, 于是跳过.
- 第三反应是使用 `std::pair` 存储下标信息, 但转念一想这样做时间复杂度大概率在常数系数意义下大于第一个方案.
- 最后选择第一个方案.
- 由于两个下标不能相同, 在找到第二个下标的过程中不仅要比较数组元素值, 还要比较当前下标是否和第一个下标相同.
- 看了题解之后意识到哈希表的大小是动态增长的, 虽然还是很大但是不会大到 1e9 的量级. 时间消耗是 $O(n)$
- 重新实现之后发现时间消耗确实减少了, 内存消耗也确实增大了.

标签: 哈希表

代码:

```cpp
class Solution {
public:
    vector<int> twoSum(vector<int> &nums, int target) {
        unordered_map<int, int> visited;
        for (int i = 0; i < nums.size(); i++) {
            int current_val = nums[i];
            int val_need_check = target - current_val;
            auto it = visited.find(val_need_check);
            if (it == visited.end()) {
                visited[current_val] = i;
            } else {
                return {it->second, i};
            }
        }
        exit(1);
    }
};
```

<div align="right"><b><a href="#toc">返回顶部↑</a></b></div>

### <a id="1.2"></a>2. 两数相加 | 中等

问题设置: 给定两个链表, 每个链表的元素都是 10 以内的非负整数, 代表一个大整数的每个十进制数码, 整个链表以逆序代表一个大整数.

要求: 以相同的链表表示方式返回这两个链表所代表的整数的和.

思路:

- 第一反应是不使用创建第三条链表的方式, 直接同时不断在两个链表中前进, 遇到 next 两个都非空的情况就照常前进, 遇到两个都是空的情况就视进位 carry 的情况创建新结点并返回, 遇到一空一非空就退出循环, 然后只在非空的链表中继续前进.
- 第二反应也想过不使用创建第三条链表的方式, 直接在短链表末尾追加新结点, 但是由于不认为这一方案会比方案一更优所以先跳过了.
- 题解采用的是方案二, 但是创建了第三条链表作为返回值. 这一方案相比方案一会为短链表额外执行许多判断语句, 但代码思维难度更低.
- 提交结果也证明了方案二确实不如方案一.

代码:

```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        ListNode* result = l1;
        int carry = 0;

        // 进入循环前保证两个指针非空:
        while (1) {
            // 求和并进位:
            int val_1 = l1->val;
            int val_2 = l2->val;
            int sum = val_1 + val_2 + carry;
            carry = sum >= 10 ? 1 : 0;
            sum = sum >= 10 ? sum - 10 : sum;
            l1->val = sum;

            // 如果下两个指针仍然非空:
            if (l1->next && l2->next) {
                l1 = l1->next;
                l2 = l2->next;

                // 继续循环:
                continue;
            }

            // 如果下两个指针为空:
            if (!l1->next && !l2->next) {
                // 说明到头了, 处理剩下的进位:
                if (carry) {
                    l1->next = new ListNode(0);
                    l1->next->val = carry;
                }

                // 直接返回:
                return result;
            }

            // 否则两个链表一长一短, 需要另外处理:
            break;
        }

        // 如果 l1 长则保持原样, 如果是 l2 长则将其嫁接到 l1 后面:
        if (l2->next) {
            l1->next = l2->next;
        }

        // 重复同样的循环:
        l1 = l1->next;
        while (1) {
            int val = l1->val;
            int sum = val + carry;
            carry = sum >= 10 ? 1 : 0;
            sum = sum >= 10 ? sum - 10 : sum;
            l1->val = sum;

            if (l1->next) {
                l1 = l1->next;
                continue;
            }

            if (carry) {
                l1->next = new ListNode(0);
                l1->next->val = carry;
            }

            return result;
        }

        exit(1);
    }
};
```

<div align="right"><b><a href="#toc">返回顶部↑</a></b></div>

### <a id="1.3"></a>3. 无重复字符的最长子串 | 中等

问题设置: 给定一个字符串, 长度的量级为 5 \* 1e4.

要求: 求字符串中满足 "字符不重复" 的最长的子串的**长度**.

思路:

- 第一反应是使用 next 数组. 既然要求一个子串中所有元素不重复, 首先知道一个元素的下一个 (不失一般性, 假设是左边的) 最近相同元素在哪会极大降低问题的实现难度. 思路是使用类似于 KMP 算法中的 next 数组那样的手法. 从当前元素开始向左延伸所能获得的不重复子串必然包含在由当前元素和左边的最近相同元素所包围起来的左开右闭范围中. 在这一范围内当前元素只有一个副本, 可以放心包含当前元素, 因此 "从当前元素开始向左延伸所能获得的不重复子串" 就等于 "在这一范围内从当前元素的左边相邻元素开始向左延伸所能获得的不重复子串" 拼接上 "当前元素". 由于能够通过状态转移求解, 本题可以归入动态规划类型.
- 求解本题的 next 数组的方法是使用一个哈希表存储从特定字符 (char) 到最近一次遇见该字符的下标 (int), 然后从左到右遍历字符串中的每个字符, 如果是首次遇见该字符则 next 值为 -1, 意义是 "可以随意向左延伸而不用担心与当前元素重复的问题"; 否则 next 值为最近一次遇见该字符的下标. 然后更新该字符的最近一次下标为当前下标并继续遍历.
- 一开始使用的哈希表是 `unordered_map`, 为的是减少思维量, 等到通过之后马上改成用整型数组 (因为 `char` 类型的值的变动范围的量级仅为 $2^8$). 优化之后的时间效率直接干爆 97.67% 的提交者.
- 第二反应是使用双指针构成滑动窗口, 但是当时并没有深入思考而是直接跳过了. 具体实现可以是利用一个哈希 (布尔型) 数组记录 (由双指针包围的) 当前的不重复子串的构成信息, 然后通过不断增大右指针从左到右遍历, 对于当前字符, 如果重复, 那么不断缩小左指针并从哈希表中弹出字符直到把当前字符的重复副本也弹出来为止, 此时子串便重新恢复了不重复的性质.

代码:

```cpp
class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        int n = s.length();

        // 边界情况:
        if (n <= 1) {
            return n;
        }

        vector<int> char2latest_idx(257, -1); // 哈希表, 存储每个字符的最新下标
        vector<int> current2previous_idx(n, -1); // next 数组, 从当前下标跳到左边最近相同字符的下标 (如果没有则跳到 -1)

        // 利用哈希表构造 next 数组:
        for (int i = 0; i < n; i++) {
            // 当前遍历到的字符:
            char &current_char = s[i];

            // 如果是首次遇见该字符:
            if (char2latest_idx[current_char] == -1) {
                // 跳到 -1:
                current2previous_idx[i] = -1;
            } else {
                // 跳到前一个相同字符的下标:
                current2previous_idx[i] = char2latest_idx[current_char];
            }

            // 更新最新下标:
            char2latest_idx[current_char] = i;
        }

        // 利用 next 数组, 采用动态规划思想, 使用滚动数组进行求解:
        int max_no_duplecate_length = 1;
        int current_no_duplecate_length = 1;
        for (int i = 1; i < n; i++) {
            // 动态规划 + 滚动数组:
            current_no_duplecate_length = min(current_no_duplecate_length + 1, i - current2previous_idx[i]);

            // 由于最终答案为所有 n 个元素开始延伸的最长不重复子串的长度的最大值, 所以直接在滚动过程中进行求解最大值:
            max_no_duplecate_length = max(max_no_duplecate_length, current_no_duplecate_length);
        }

        return max_no_duplecate_length;
    }
};
```

<div align="right"><b><a href="#toc">返回顶部↑</a></b></div>

### <a id="1.4"></a>4. 寻找两个正序数组的中位数 | 困难

问题设置: 给定两个升序排序的有序整型数组, 长度均为 1e3 量级.

要求: 返回由这两个数组构成的有序大数组中的中位数. 时间复杂度能优化到 $O(\log (m + n))$ 最好.

思路:

- 第一反应是分割的思路, 将两个数组 (假设一上一下水平并列) 分割为左上, 右上, 左下, 右下四个部分, 其中左上和左下构成逻辑上的合并数组的左半部分, 而右上和右下构成合并数组的右半部分. 一个正确的分割需要满足两个因素:
  - 分割的性质: 左上和左下的所有元素必须小于等于右上和右下的所有元素. 这一条件等价于 "左上和左下的最大元素小于等于右上和右下的最小元素".
  - 分割的大小: 由于求的是**合并数组的中位数**, 左上和左下的元素数量加起来应该等于总数量的一半 (细节等到实现的时候再考虑).
- 自己的实现是使用**解耦**的双指针在两个数组中进行二分查找, 后来证明这个方案不仅思维难度高, 实现起来也是错误百出. 但是由于在实现的过程中还是巩固了一些知识, 认识到了自己的一些不足, 因此还是很有必要将其记录下来. 真要做还是使用**耦合**的双指针, 思维难度直接下降几个量级.
  - 首先是二分法的一些思考:
    - 区间的标记习惯:
      - 我自己使用的是左闭右开的区间表示习惯, 即使用下标 `left` 和 `right` 标记范围为 `[left, right)` 的范围.
    - 二分法的过程归纳 (不失一般性, 总是假设当前要进行二分的子数组的左端点下标 `left` 等于 `0`):
      - 排他性二分法:
        - `right >= 3`: 转化为 `right == 1` 或 `right == 2` 或 `right >= 3`
        - `right == 2`: 转化为 `right == 0` 或 `right == 1`
        - ~~`right == 1`: 边界情况, 需要手动判定~~ (统一纳入下面的情况)
        - ~~`right == 0`: 边界情况, 需要手动判定~~ (统一纳入下面的情况)
        - `right <= 1`: 边界情况, 需要手动判定
      - 非排他性二分法:
        - `right >= 3`: 转化为 `right == 2` 或 `right >= 3`
        - ~~`right == 2`: 往左需要手动判定, 往右转化为 `right == 1`~~ (统一纳入下面的情况)
        - ~~`right == 1`: 需要手动判定~~ (统一纳入下面的情况)
        - `right <= 2`: 边界情况, 需要手动判定
  - 然后是对于本题**解耦的**双指针二分法的思路:
    - 如果不满足分割性质 (排他性二分法):
      - 如果分割大小 "左小右大":
        - 必然要增大左边小边
      - 如果分割大小 "左大右小":
        - 必然要减小左边大边
    - 如果满足分割性质 (非排他性二分法):
      - 如果分割大小 "左小右大":
        - 左边大边和小边同时增大
      - 如果分割大小 "左大右小":
        - 左边大边和小边同时减小
- 看完题解之后发现自己的思路中 "分割" 部分对了, 而 "双指针" 部分则走歪了. 实际上由于要求的分割必然需要满足其大小等于合并数组一半的条件, 两个指针应该是耦合的, 只需要对一个指针进行二分即可. 自己一开始的做法相当于同时需要满足分割大小条件和分割性质条件, 而题解则是在手里捏着已经满足的分割大小条件的情况下仅仅需要满足分割性质条件, 这样做直接把思维难度下降了无数个量级.
- 题解的第二个做法类似于 "使用分治法求有序数组中第 k 大数", 但是本题中由于是双数组, 所以分治的判断条件比较脑筋急转弯. 大致想法是选择一个本来就小于 k 的分割 (例如左上和左下都是 `k / 2 - 1` 的分割), 如果这个分割符合性质, 那就全部收入囊中, 问题转化为求第 `k - 2 * (k / 2 - 1)` 大的数; 如果不符合性质, 那么可以通过裁剪最大值较大的子数组得到一个新的满足性质的分割, 例如左上小于左下, 那么可以裁剪左下直到新分割符合性质, 但是无论如何左上都是不变的, 反过来如果左上大于左下则左下无论如何都是不变的, 结合起来就是最大值较小的子数组可以收入囊中, 问题转化为求第 `k - (k / 2 - 1)` 大的数. 由于自己没有实现这个方案, 所以不知道具体的边界细节, 这里就先不讨论.
- 这道题做了一个下午, 以一种很遗憾的方式达成了**一道困难做一天**的成就.

代码:

```cpp
class Solution {
public:
    double findMedianSortedArrays(vector<int> &nums1, vector<int> &nums2) {
        // 边界情况:
        if (nums1.empty() || nums2.empty()) {
            const auto &nums = nums1.empty() ? nums2 : nums1;
            int size = nums.size();
            return size % 2 ? nums[size / 2] : (nums[size / 2 - 1] + nums[size / 2]) / 2.0;
        }

        // 总是使得数组 1 最长, 降低思维难度:
        if (nums1.size() < nums2.size()) {
            swap(nums1, nums2);
        }

        // 优化时间性能:
        int nums1_size = nums1.size();
        int nums2_size = nums2.size();

        int total_size = nums1_size + nums2_size;
        int threshold = total_size / 2;
        bool is_odd = total_size % 2;

        // 对数组 1 进行二分:
        int left = max(0, threshold - nums2_size); // 最左端并不一定是 0, 因为有可能整个数组 2 的元素全部纳入都不够
        int right = min(nums1_size, threshold) + 1; // 最右端同理
        int cut_1, cut_2;
        while (1) {
            // 分别对数组 1 和数组 2 进行切割:
            cut_1 = left + (right - left) / 2;
            cut_2 = threshold - cut_1;

            // 左上和左下的最大值:
            int left_max = get_left_max(nums1, nums2, cut_1, cut_2);

            // 右上和右下的最小值:
            int right_min = get_right_min(nums1, nums2, cut_1, cut_2, nums1_size, nums2_size);

            // 如果分割符合性质直接退出:
            if (left_max <= right_min) {
                break;
            }

            // 否则需要确定往左二分还是往右二分:
            bool is_nums1_bigger = cut_1 == 0 ? false : (cut_2 == 0 ? true : nums1[cut_1 - 1] > nums2[cut_2 - 1]);
            left = is_nums1_bigger ? left : cut_1 + 1; // 条件传送
            right = is_nums1_bigger ? cut_1 : right; // 条件传送
        }

        int left_max = get_left_max(nums1, nums2, cut_1, cut_2);
        int right_min = get_right_min(nums1, nums2, cut_1, cut_2, nums1_size, nums2_size);

        return is_odd ? right_min : (left_max + right_min) / 2.0;
    }

    inline int get_left_max(const vector<int> &nums1, const vector<int> &nums2, const int cut_1, const int cut_2) {
        return cut_1 == 0 ? nums2[cut_2 - 1]
                          : (cut_2 == 0 ? nums1[cut_1 - 1] : max(nums1[cut_1 - 1], nums2[cut_2 - 1]));
    }

    inline int get_right_min(const vector<int> &nums1, const vector<int> &nums2, const int cut_1, const int cut_2,
                             const int nums1_size, const int nums2_size) {
        return cut_1 == nums1_size ? nums2[cut_2]
                                   : (cut_2 == nums2_size ? nums1[cut_1] : min(nums1[cut_1], nums2[cut_2]));
    }
};
```

<div align="right"><b><a href="#toc">返回顶部↑</a></b></div>

### <a id="1.5"></a>5. 最长回文子串 | 中等

问题设置: 给定一个字符串, 长度量级为 1e3.

要求: 返回最长回文子串.

思路:

- 一般的单双中心向两边拓展的动态规划的算法早就做烂了, 这里直接使用 Manacher 算法.
- Manacher 算法采用的也是动态规划的思想, 但是和一般的动态规划算法只往一个方向拓展不同, Manacher 算法利用的性质是回文子串的对称性, 在迭代过程中维护一个右端点最靠右的回文子串, 如果当前遍历到的字符包含在这个右端点最靠右的回文子串中, 那么可以利用当前字符关于右端点最靠右回文子串的中心的对称点的信息对当前字符的回文半径进行初始化, 也就是转移了状态.
- 细节一: 右端点最靠右回文子串只负责其覆盖半径内的信息, 对于覆盖半径外的信息其一概不知 (因为其右端点之外的信息实际上都还没有被遍历过), 所以当前字符初始化的回文半径的初始化值实际上是其 "对称点的回文半径" 和 "对称点距离右端点最靠右回文子串的左端点的距离" 之间的较小值.
- 细节二: 对于遍历到的每一个点, 如果其位于右端点最靠右回文子串的覆盖范围内, 并且对称点的回文范围是右端点最靠右回文子串的覆盖范围的真子集, 那么无需再对其回文半径进行拓展; 反之如果该点位于覆盖半径之外或者其对称点的回文半径触及了右端点最靠右回文子串的左端点, 那么就需要对其进行拓展. 如果能够拓展出去, 那么当前字符就成为新的右端点最靠右回文子串. 由于要么不用拓展, 要么直接拓展完使得拓展范围内的字符不用拓展, 整体的时间复杂度为 $O(n)$.
- 细节三: 由于 Manacher 算法需要对初始字符串进行插入记号 (marker) (一般是字符 `#`) 的预处理, 在求得最长回文子串之后若要转换回原字符串需要在预处理后的字符串和原字符串的下标和回文范围之间进行正确的映射.
  - 对于回文范围, 假设预处理后的字符串的最大回文子串的回文半径 (注意这里是回文半径) 是 `best_P_i`, 通过在草稿纸上简单画图可知该回文子串的右半部分的非 `#` 字符总是可以插入到左半部分的 `#` 字符中, 最后对应到原字符串中的回文范围 (注意这里是回文范围) 总是等于 `best_P_i - 1`.
  - 对于下标, 很容易可推知预处理后的字符串映射回原字符串只需要将下标整除以 2 即可.
    - 原字符串的最长回文子串的左端点可以通过先计算预处理后的字符串的最长回文子串的左端点然后映射回原字符串的方法计算得到.
- 细节四: 右端点最靠右回文子串并不是最长回文子串, 右端点最靠右回文子串的作用只是为了转移状态.
- 细节五: 关于是否需要对原字符串进行预处理, 自己原先是比较疑惑的, 看了[这篇帖子](https://stackoverflow.com/questions/37811437/manachers-algorithm)之后我的想法是在个人实现的时候需要预处理, 正如帖子里那位老哥所说的, 算法本身已经很饶舌了再不预处理一下直接变成天书, 写的人写不懂看的人更看不懂. 如果是生产级别的代码那该优化优化, 不过那就是另一回事了.

代码:

```cpp
class Solution {
public:
    string longestPalindrome(string s) {
        // 对原字符串进行备份:
        string s_temp = s;

        // 预处理, 添加 `#` 标记:
        s = add_marker(s);
        int n = s.length();

        // 右端点最靠右回文子串:
        int C = -1;
        int R = 1;
        int C_left_end = C - R + 1; // 左端点

        // 存储每个字符串的回文半径的数组:
        vector<int> P(n, 1);

        // 最长回文子串:
        int best_i = -1;
        int best_P_i = 1;

        // 遍历每个字符:
        for (int i = 0; i < n; i++) {
            char c = s[i];

            int P_i_temp = 1; // 减少内存读写

            // 如果位于右端点最靠右回文子串的覆盖范围内:
            if (i <= C + R - 1) {
                // 求对称点:
                int i2 = 2 * C - i;

                // 对称点的回文半径:
                int P_i2 = P[i2];

                // 如果对称点的回文范围是真子集:
                if (C_left_end < i2 - P_i2 + 1) {
                    // 当前字符无需拓展:
                    P[i] = P_i2;
                    continue;
                }

                // 否则初始化, 准备拓展:
                P_i_temp = i2 - C_left_end + 1;
            }

            // 拓展当前字符的回文半径:
            while (i - P_i_temp >= 0 && i + P_i_temp <= n && s[i - P_i_temp] == s[i + P_i_temp] && ++P_i_temp){}

            P[i] = P_i_temp;

            // 更新右端点最靠右回文子串:
            if (C + R < i + P_i_temp) {
                C = i;
                R = P_i_temp;
                C_left_end = C - R + 1;
            }

            // 更新最长回文子串:
            if (best_P_i < P_i_temp) {
                best_i = i;
                best_P_i = P_i_temp;
            }
        }

        // 将预处理后的字符串映射回原字符串:
        int __n = best_P_i - 1;
        int __pos = (best_i - best_P_i + 1) / 2;

        return s_temp.substr(__pos, __n);
    }

    string add_marker(const string &s) {
        string s2;
        for (const auto &c : s) {
            s2.push_back('#');
            s2.push_back(c);
        }
        s2.push_back('#');
        return s2;
    }
};
```

Manacher 算法做得非常快, 而上面的 "4. 寻找两个正序数组的中位数" 却做了一下午. 这也体现了自己的一个做题的特点就是特别不擅长边界条件多的思路.

<div align="right"><b><a href="#toc">返回顶部↑</a></b></div>

### <a id="1.6"></a>10. 正则表达式匹配 | 困难

问题设置: 给定一个字符串 `s` 和一个正则表达式模式串 `p`, 两者长度均小于 20. 其中 `p` 仅包含两种模式, `.` (匹配一个任意字符) 和 `*` (匹配任意个特定字符), 并且保证 `*` 前面跟着一个字符. 需要注意的是 `*` 前面跟着的字符有可能是 `.`.

要求: 返回模式串 `p` 是否能够完全匹配 `s`.

思路:

- 第一反应就是使用动态规划.
- 首先要做的是将模式串的两种长度不同的零件 `<char>` 和 `<char>*` 抽象为统一的零件. 这可以通过自定义一个模式类 `Pattern` 来实现.
- 之后使用下标 `i` 索引模式串的零件, 使用下标 `j` 表示字符串 `s` 的范围为 `s[0 : j - 1]` 的子串, 使用数组 `dp[i][j]` 进行状态转移. 现在假设 `i` 固定, 对于每个 `j`, 状态转移方程分为两部分:
  - 如果当前零件是匹配固定字符 (必须匹配 1 个字符), 那么对于 `.` 来说任意非空子串都能转移状态至子串 `s[0 : j - 2]`, 除了空子串, 空子串必定失配 (因为必须要匹配一个字符, 而空子串没有字符); 而对于其他任意字符而言当且仅当最后一个字符 `s[j - 1]` 与当前字符相同时非空字串能够转移状态, 而空子串仍然必定失配.
  - 如果当前零件是带星号字符 (可能匹配 0 或多个字符), 那么不论子串是空子串还是非空子串都需要尝试匹配, 因为一次可以吞掉 0 个或多个相同字符 (`s[j - 1]`, `s[j - 2]`, ...), 并且每吞掉一个字符都需要进行一次状态转移, 只要这些转移状态后的其中一种子情况能够匹配那么当前子串 `s[0 : j - 1]` 就能够匹配. 也就是说对于带星号零件而言匹配过程是个双循环.

代码:

```cpp
// 自定义的模式类:
class Pattern {
private:
    int _length;
    vector<string> parts;

public:
    size_t length() {
        return _length;
    }
    string get_part_by_index(int index) {
        if (index < 0 || index >= _length) {
            throw out_of_range("");
        }
        return parts[index];
    }
    Pattern(const string &pattern) {
        _length = 0;
        int i = 0;
        int pattern_length = pattern.length();

        // 提取所有零件:
        while (i < pattern_length) {
            char c = pattern[i];
            i++;
            string part({c});
            if (i < pattern_length && pattern[i] == '*') {
                part.push_back('*');
                i++;
            }
            parts.emplace_back(part);
            _length++;
        }
    }
};

class Solution {
public:
    bool isMatch(string s, string p) {
        auto my_pattern = Pattern(p);
        int s_length = s.length();
        int p_length = my_pattern.length();
        vector<bool> dp(s_length + 1, false);
        dp[0] = true;

        // 遍历每个零件:
        for (int i = 0; i < p_length; i++) {
            // 获取零件:
            string part = my_pattern.get_part_by_index(i);
            int part_length = part.length();

            // 固定字符 (必须匹配 1 个字符):
            if (part_length == 1) {
                char c = part[0];

                // 匹配任意字符 (单次):
                if (c == '.') {
                    // 任意非空子串都能转移状态:
                    for (int j = s_length; j >= 1; j--) {
                        dp[j] = dp[j - 1];
                    }

                    // 空子串失配:
                    dp[0] = false;
                }

                // 匹配特定字符 (单次):
                else {
                    // 仅 "最后一个字符与当前字符相同" 的非空字串能够转移状态:
                    for (int j = s_length; j >= 1; j--) {
                        dp[j] = c == s[j - 1] ? dp[j - 1] : false;
                    }

                    // 空子串必定失配:
                    dp[0] = false;
                }
            }

            // 带星号字符 (可能匹配 0 或多个字符):
            else {
                char c = part[0];

                // 注意此处同样能够匹配空字串:
                for (int j = s_length; j >= 0; j--) {
                    // 匹配 0 个字符:
                    if (dp[j]) {
                        continue;
                    }

                    // 尝试匹配多个字符:
                    bool dp_j = false;
                    for (int k = j - 1; k >= 0 && (c == '.' || c == s[k]) && !(dp_j = dp[k]); k--) {
                    }
                    dp[j] = dp_j;
                }
            }
        }
        return dp[s_length];
    }
};
```

<div align="right"><b><a href="#toc">返回顶部↑</a></b></div>

### <a id="1.7"></a>11. 盛最多水的容器 | 中等

问题设置: 给定 `n` 个非负整数, 分别代表坐标轴上 `x = 0`, `x = 1`, ..., `x = n - 1` 处的 "墙壁" 高度. `n` 的量级为 1e5.

要求: 返回使用其中任意两个墙壁和底部 x 轴构成的桶所能装的水的最大体积.

思路:

- 这道题应该列入困难题. 我认为的困难题要么确实是很难, 要么是那种脑子转不过来的时候怎么都做不出来的题. 本题明显属于后者.
- 第一反应是单调栈, 但是有反例: `[1, 2, 2, 1]`. 单调栈无法解决这种中间凸的情况.
- 第二反应是由外至内的双指针, 虽然这一方案确实是正确方案, 但是当时自己认为对于墙壁高度分布对称的情况这一方案无法计算下一步而放弃了这一方案.
- 第三反应是由左至右的双指针, 其中右指针负责外循环, 左指针负责内循环. 固定右指针, 左指针沿着向左的递减序列不断向左边递减; 而右指针则沿着右边的递减序列不断向右边递减. 这一方案虽然能够通过时间限制, 但时间复杂度依然很高.
- 最后看了题解发现第二个方案是正确的. 当选择了左右两端的墙壁 A 和 B 之后, 较矮的墙壁 (假设为 A) 的潜力就已经发挥完全了, 这是因为桶的高度等于两个墙壁的高度的较小值, 若将右指针向内移动, 如果 B 变高, 桶的高度不会增加 (因为取决于较小值, 而较小值 A 此时不变), 如果 B 变矮, 桶的高度不仅不会增加反而还有可能减小, 而宽度无论如何都是减小的, 所以对于 A 来说, 和 B 计算完一次桶的体积之后 A 就完全可以 "弃用" 了. 至于本题的双指针做法仅仅是基于所有这些推导之上的手段罢了. 本题非常取巧, 建议背诵, 不建议理解.
- 为什么由内向外不行而由外向内却可以, 自己思考了一下认为原因是题目要求的是最大值, 而由内向外的做法会造成桶的宽度的增加因此每次都需要重新检查, 而由外向内的做法桶的宽度是减小的, 因此能做到一步到位.
- 从本题学习到的思想和 "4. 寻找两个正序数组的中位数" 类似, 都是要尽量捏住问题的一个维度 (题目 "4. 寻找两个正序数组的中位数" 中是分割的大小保持不变, 本题中是桶的宽度由大到小遍历).

代码:

```cpp
class Solution {
public:
    int maxArea(vector<int>& height) {
        int l = 0;
        int r = height.size() - 1;
        int result = 0;
        while(l < r){
            int height_l = height[l];
            int height_r = height[r];
            result = max(result, min(height_l, height_r) * (r - l));
            int left_adjust = height_l < height_r ? 1 : 0;
            l += left_adjust;
            r -= (1 - left_adjust);
        }
        return result;
    }
};
```

<div align="right"><b><a href="#toc">返回顶部↑</a></b></div>

### <a id="1.8"></a>105. 从前序与中序遍历序列构造二叉树 | 中等

问题设置: 给定一个二叉树的前序序列 `preorder` 和中序序列 `inorder`, 其中二叉树不含重复元素. 二叉树结点个数的量级为 1e3.

要求: 返回重建的二叉树.

思路:

- 非常经典的重建二叉树, 同时也十分简单, 直接使用分治法, 先递归生成左右子树然后拼装在一起形成一棵完整的树.
- 由于已经做过多次并且思路非常明确, 直接五分钟秒了.

代码:

```cpp
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    TreeNode *buildTree(vector<int> &preorder, vector<int> &inorder) {
        int n = preorder.size();
        return _buildTree(preorder, inorder, 0, n, 0, n);
    }
    TreeNode *_buildTree(vector<int> &preorder, vector<int> &inorder, int preorder_left, int preorder_right,
                         int inorder_left, int inorder_right) {
        if (preorder_left == preorder_right) {
            return nullptr;
        }
        int val = preorder[preorder_left];
        int left_sub_tree_length =
            find(inorder.begin() + inorder_left, inorder.begin() + inorder_right, val) - inorder.begin() - inorder_left;
        auto new_node = new TreeNode(val);
        new_node->left = _buildTree(preorder, inorder, preorder_left + 1, preorder_left + 1 + left_sub_tree_length,
                                    inorder_left, inorder_left + left_sub_tree_length);
        new_node->right = _buildTree(preorder, inorder, preorder_left + 1 + left_sub_tree_length, preorder_right,
                                     inorder_left + left_sub_tree_length + 1, inorder_right);
        return new_node;
    }
};
```

<div align="right"><b><a href="#toc">返回顶部↑</a></b></div>

### <a id="1.9"></a>26. 删除有序数组中的重复项 | 简单

问题设置: 给定一个非严格递增的整数数组 `num`, 数组长度的量级为 1e4.

要求: 对给定的数组进行**原地**修改, 对数组中的元素进行去重, 修改后的数组应为严格递增, 返回修改后的新数组长度. 注意返回的是新数组的**长度** (假设为 `N`), 而原数组从开头开始数总共 `N` 个整型元素的空间将用于存放新数组.

思路:

- 使用双指针, 其中 `right` 指针负责在前面不断比较相邻元素, 而 `left` 指针负责在后面接已经被 `right` 指针确认是唯一的值.

代码:

```cpp
class Solution {
public:
    int removeDuplicates(vector<int> &nums) {
        int left_ptr = 0;
        int right_ptr = 0;
        int n = nums.size();
        while (1) {
            // 进入前需要确保 nums_at_right_ptr == nums[right_ptr], 而循环过程中 nums_at_right_ptr 必然保持不变:
            while (right_ptr < n - 1 && nums[right_ptr] == nums[right_ptr + 1]) {
                right_ptr++;
            }

            // 一旦退出循环, 要么遍历到了末尾, 要么相邻两个元素不相等.
            // 但是无论哪种情况 nums_at_right_ptr 代表的都是同值元素的最后一个元素, 可以直接赋值:
            nums[left_ptr] = nums[right_ptr];
            left_ptr++;

            // 如果相邻两个元素不相等:
            if (right_ptr < n - 1) {
                right_ptr++;
            }

            // 如果到了末尾:
            else {
                // 直接退出:
                break;
            }
        }
        return left_ptr;
    }
};
```

<div align="right"><b><a href="#toc">返回顶部↑</a></b></div>

### <a id="1.10"></a>80. 删除有序数组中的重复项 II | 中等

问题设置: 给定一个非严格递增的整型数组, 数组长度的量级为 1e4.

要求: 对给定的数组进行**原地**修改, 删减数组中出现次数大于等于两次的元素使其只出现两次, 修改后的数组应为严格递增, 返回修改后的新数组长度. 注意返回的是新数组的**长度** (假设为 `N`), 而原数组从开头开始数总共 `N` 个整型元素的空间将用于存放新数组.

思路:

- 一开始的思路还是像 "26. 删除有序数组中的重复项" 那样, 对右指针的遍历状态进行检查, 具体来说如果从右指针开始往右数连续三个元素都相同的话那就递增右指针, 如果右指针停下来了那么对这三个元素互相之间的相等情况分类讨论. 这种方法比较直观, 但是实现起来思维难度很大, 有很多边界情况要考虑, 并且最后提交的运行效率也并不高.
- 由于实在不知道还能如何优化这道题的算法, 于是跑去看了题解, 一看发现果然是需要切换考虑问题的视角. 题解的视角是从 "左指针往左至多保留两个相同元素" 出发的, 而前一个方案是从 "检查右指针所指的元素开始向右是否有连续两个相同元素" 出发的. 具体来说假设当前遍历到了一个整数 val, 如果当前还没压满两个等于 val 的整数, 那么完全可以压入当前这个 val, 反之如果已经压满了两个那就跳过. 如何检查压没压满呢? 直接检查左指针往左数第二个元素即可. 这种方案不仅思维难度低, 实现起来也非常简洁, 代码运行效率也非常高.

代码:

```cpp
class Solution {
public:
    int removeDuplicates(vector<int> &nums) {
        if (nums.size() <= 2) {
            return nums.size();
        }

        const int nums_size = nums.size();
        int left_ptr = 2;
        int right_ptr = 2;
        while (right_ptr < nums_size) {
            if (nums[left_ptr - 2] != nums[right_ptr]) {
                nums[left_ptr++] = nums[right_ptr];
            }
            right_ptr++;
        }
        return left_ptr;
    }
};
```

<div align="right"><b><a href="#toc">返回顶部↑</a></b></div>

### <a id="1.11"></a>69. x 的平方根 | 简单

问题设置: 给定一个非负 `int` 整数 `x`, 其量级为 1e31.

要求: 返回不超过 `x` 的算术平方根的最大整数.

思路:

- 第一反应是二分查找, 思想很简单, 但是边界条件需要格外注意. 我自己还是采用了左闭右开的区间表示方式, 即使用 `left_end` 和 `right_end` 表示区间 `[left_end, right_end)`. `x` 的算术平方根将整个查找范围划分为左边 "不超过算术平方根的整数" 和右边 "超过算数平方根的整数" 两部分, 所以此处使用的二分法是**仅右排他**的二分法, 对查找范围的大小进行脑内分情况讨论之后会发现 `>= 3` 的情况会转化为 `== 2` 和 `== 1` 的情况, `== 2` 的情况会转化为 `== 1` 的情况, 而 `== 1` 的情况为边界情况, 此时必然有 `left_end` 为正确答案, 实际上由于左不排他性, 查找范围中必然含有 "不超过算术平方根的整数" 的右端点, 当查找范围的大小为 `1` 时其中唯一的元素只能是该右端点, 而根据题目要求, 该右端点就是正确答案.
- 第二反应是牛顿迭代法, 但是我自己实际上是有点抗拒这种方法的, 因为我对一般的离散算法有一种 "离散而精确" 的 "手感", 这和我对微分方程数值解中的数值算法有一种 "连续而近似" 的 "手感" 一样. 我非常偏向于离散而精确的手感, 同时即使讨厌连续而近似的手感也以 "这是在计算机有限精度的限制下在微分方程数值解中能够使用的唯一方案" 为理由而妥协. 但是在能够离散而精确的情况下让我选择连续而近似的解法就有点难受了. 不过很幸运, 我还能够以 "这样做能够击败 100% 用户" 为理由继续妥协下去.
- 此外牛顿迭代法的解法有点类似于在求斐波那契数列时使用通项公式, 这就不是什么二分法或者动态规划了而是直接使用的纯数学解法 (虽然斐波那契数列的矩阵解法也是数学解法但其至少结合了快速幂算法).
- 二分法和牛顿法最后的提交结果差不多, 都是能够击败 100%, 但是数学上来讲牛顿法肯定是更快的, 因为它是二次收敛 (虽然在 `x == 0` 的时候有重根而收敛速率下降 (具体下降至什么程度忘记了但至少不再是二次收敛) 但由于将初始值恰恰设置为了 `0` 因此完美抵消了这一边界情况). 下面代码选择的是二分法的方案.
- 看了题解发现还有第三种解法, 就是使用指数函数和对数函数将幂函数转化为等价形式, 绕过题目要求的限制 (不允许使用 `pow` 函数但没说不允许 `exp` 函数). 这有点投机取巧了.

代码:

```cpp
class Solution {
public:
    int mySqrt(int x) {
        typedef long long ll;

        ll left_end = 0;
        ll right_end = INT_MAX + (ll)1;
        while (1) {
            if (left_end + 1 == right_end) {
                return left_end;
            }

            ll mid = left_end + (right_end - left_end) / 2;
            if (mid * mid > x) {
                right_end = mid;
            } else {
                left_end = mid;
            }
        }
        return -1;
    }
};
```

<div align="right"><b><a href="#toc">返回顶部↑</a></b></div>

### <a id="1.12"></a>124. 二叉树中的最大路径和 | 困难

问题设置: 给定一棵二叉树, 树的结点的值的类型为整型 `int`, 结点数量的量级为 1e4, 结点的值的范围可正可负, 而绝对值的量级不超过 1e3. 树中的**路径**定义为一个结点序列, 序列中前后相邻的两个结点之间均存在边. 注意这个结点序列可以是任意顺序的, 例如可以从左子结点开始, 经过根结点, 再到右子结点构成一个序列, 也可以返过来. 相当于把树看成是一个无向无环图. **路径和**定义为路径中所有结点的值之和.

要求: 返回树中存在的最大路径和.

思路:

- 第一反应是将问题分解为左子树和右子树的两个子问题, 然后在根结点处合并.
- 由于路径可以位于任意位置, 因此首先考虑对路径位置进行降维:

  - 假设路径经过根结点, 那么最大路径和取决于 "**左子树中**以左子树根结点为端点的最大路径和" 和 "**右子树中**以右子树根结点为端点的最大路径和". 只要哪个大于 0 就加上哪个, 多多益善; 小于等于 0 的路径和起到反作用, 因此不考虑.
  - 假设路径不经过根结点, 那么路径就被根结点阻挡在左子树或者右子树中, 因此最大路径和等于 "**左子树中**的最大路径和" 和 "**右子树中**的最大路径和" 之间的较大者.

  可以看到降维之后的子问题需要维护两个返回值, 一个是 "以根结点为端点的最大路径和", 另一个是 (无任何限制的) "最大路径和". "最大路径和" 的维护方法如上所示, 而 "以根结点为端点的最大路径和" 就等于根结点的值加上左右子树中以根结点为端点的最大路径和的较大者.

- 上面考虑的是左右子树均为非空的情况. 如果左右子树均为空, 那么不论是最大路径和还是以根结点为端点的最大路径和均等于根结点的值; 如果左右子树中某一个为空而另一个为非空, 同样可以根据上述思路进行分情况讨论.
- 这道题目此前已经做过. 但是现在并不是依靠当时的做题经验 (事实上我在做完之后返回去看当时自己的做法时是有新鲜感的), 而是依靠的自己做过的树的题目所积攒起来的手感.

代码:

```cpp
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    int maxPathSum(TreeNode *root) {
        int mps_all;
        int mps_root;
        _maxPathSum(root, mps_all, mps_root);

        return mps_all;
    }

    // 帮手函数
    void _maxPathSum(TreeNode *root, int &mps_all, int &mps_root) {
        // 左右子树均为空:
        if (!root->left && !root->right) {
            // 不论是最大路径和还是以根结点为端点的最大路径和均等于根结点的值:
            mps_all = mps_root = root->val;

            return;
        }

        // 左右子树中某一个为空而另一个为非空:
        if (!root->left || !root->right) {
            // 选定非空子树:
            TreeNode *sub_tree = root->left ? root->left : root->right;

            // 求解子问题:
            int mps_all_sub_tree;
            int mps_root_sub_tree;
            _maxPathSum(sub_tree, mps_all_sub_tree, mps_root_sub_tree);

            // 构造结果:
            mps_root = root->val + max(0, mps_root_sub_tree);
            mps_all = max(mps_all_sub_tree, mps_root);

            return;
        }

        // 左右子树均为非空.

        // 求解左子树的子问题:
        int mps_all_left;
        int mps_root_left;
        _maxPathSum(root->left, mps_all_left, mps_root_left);

        // 求解右子树的子问题:
        int mps_all_right;
        int mps_root_right;
        _maxPathSum(root->right, mps_all_right, mps_root_right);

        // 构造结果:
        mps_all = max(max(mps_all_left, mps_all_right), root->val + max(0, mps_root_left) + max(0, mps_root_right));
        mps_root = root->val + max(0, max(mps_root_left, mps_root_right));

        return;
    }
};
```

<div align="right"><b><a href="#toc">返回顶部↑</a></b></div>

### <a id="1.13"></a>102. 二叉树的层序遍历 | 中等

问题设置: 给定一棵二叉树 `root`, 其结点数目的量级为 1e3, 结点的值为整数, 可正可负, 取值范围的绝对值的量级为 1e3.

要求: 按层序遍历顺序返回所有结点的值, 其中每一层结点的值构成一个数组, 最终的返回值为一个由所有层的结点值数组构成的数组. 例如传入一棵三层的树 `[3,9,20,null,null,15,7]` 所返回的值应为 `[[3],[9,20],[15,7]]`.

思路:

- 主要思路是维护一个循环不变量: "前一层的所有非空树结点指针队列", 记为 A.
- 每次进入循环时对 A 进行遍历, 在收集前一层的所有结点的值至一个数组中的同时收集当前层的所有非空树结点于另一个队列 B. 在循环的最后一步将 B 赋值给 A 维护循环不变量.
- 初始时 A 等于 `root`; 循环退出当且仅当 B 为空.

代码:

```cpp
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    vector<vector<int>> levelOrder(TreeNode *root) {
        if (!root) {
            return {};
        }

        queue<TreeNode *> last_layer_tree_node_pointers;  // 前一层的所有非空树结点指针队列 A
        queue<TreeNode *> current_layer_tree_node_pointers;  // 当前层的所有非空树结点指针队列 B
        last_layer_tree_node_pointers.push(root);  // 初始时 A 等于 `root`
        vector<vector<int>> result;
        while (1) {
            vector<int> last_layer_tree_node_pointer_values;

            // 对 A 进行遍历:
            while (!last_layer_tree_node_pointers.empty()) {
                auto node = last_layer_tree_node_pointers.front();
                last_layer_tree_node_pointers.pop();

                // 收集前一层的所有结点的值:
                last_layer_tree_node_pointer_values.push_back(node->val);

                // 收集当前层的所有非空树结点:
                if (node->left) {
                    current_layer_tree_node_pointers.push(node->left);
                }
                if (node->right) {
                    current_layer_tree_node_pointers.push(node->right);
                }
            }

            result.emplace_back(std::move(last_layer_tree_node_pointer_values));

            // 循环退出当且仅当 B 为空:
            if (current_layer_tree_node_pointers.empty()) {
                break;
            }

            // 否则将 B 赋值给 A, 维护循环不变量:
            swap(last_layer_tree_node_pointers, current_layer_tree_node_pointers);
        }

        return result;
    }
};
```

<div align="right"><b><a href="#toc">返回顶部↑</a></b></div>

### <a id="1.14"></a>199. 二叉树的右视图 | 中等

问题设置: 给定一棵二叉树 `root`, 其结点数目的量级为 1e2, 结点的值为整数, 可正可负, 取值范围的绝对值的量级为 1e2.

要求: 以数组的形式, 按从上到下的顺序, 返回树中每一层从右往左数第一个结点的值.

思路:

- 依照直觉, 似乎按从右往左的顺序进行前序遍历能够按照所要求的顺序遍历树中每一层从右往左数第一个结点. 理论上也确实如此, 对于按从右往左的顺序进行前序遍历, 有如下定理成立:
  - **定理**: 对于按从右往左的顺序进行前序遍历, 其在每一层中首次遍历到的结点必定是该层中最右端的结点.
    **证明**: 假设对于按从右往左的顺序进行前序遍历, 其在某一层中首次遍历到的结点不是该层中最右端的结点. 由于该层中最右端的结点位于该层中首次遍历到的结点的右方, 因此必然能够找到二者的最近公共祖先, 使得该层中首次遍历到的结点位于二者的最近公共祖先的左子树中, 而该层中最右端的结点位于二者的最近公共祖先的右子树中. 按照从右往左的顺序进行前序遍历的性质, 一棵树的左子树中存在已被遍历的结点当且仅当该树的右子树中的所有结点均已被遍历, 然而该层中首次遍历到的结点却先于该层中最右端的结点被遍历, 这便产生了矛盾.
    因此只需按照从右往左的顺序进行前序遍历并在首次进入某一层时收集当前结点即可. 由于前序遍历总是从上到下的, 因此收集到的所有的最右端结点的序列天然是按照高度排序好的.

代码:

```cpp
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    vector<int> rightSideView(TreeNode *root) {
        if (!root) {
            return {};
        }
        vector<int> result;
        int best_level = 0;
        _rightSideView_helper(root, 1, best_level, result);
        return result;
    }

    // 按从右往左的顺序进行前序遍历:
    void _rightSideView_helper(TreeNode *root, int level, int &best_level, vector<int> &result) {
        // 在首次进入某一层时收集当前结点:
        if (level > best_level) {
            best_level++;
            result.push_back(root->val);
        }

        // 遍历右子树:
        if (root->right) {
            _rightSideView_helper(root->right, level + 1, best_level, result);
        }

        // 遍历左子树:
        if (root->left) {
            _rightSideView_helper(root->left, level + 1, best_level, result);
        }
    }
};
```

<div align="right"><b><a href="#toc">返回顶部↑</a></b></div>
