---
layout: "course-resource"
title: "Week 1 Reference Sheets"
title_ko: "1주차 공통 참고표"
permalink: "/courses/practical-algorithms/reference/"
course_id: "practical-algorithms"
---

## Operation costs

Let n be input length, d the number of distinct values, and q the number of copied entries. Integer arithmetic and integer hashing are treated as constant cost.

| Operation | Time | Storage / condition |
| --- | --- | --- |
| List indexing | O(1) | Direct position access |
| List membership | O(n) | Sequential value comparisons |
| dict/set lookup and update | Expected O(1), worst O(n) | Hashable keys; long-key hashing has its own cost |
| Copy q entries | O(q) | O(q) shallow reference copy |
| Sort n entries | Worst O(n log n) | O(n) Python workspace |
| Store latest position per value | Expected O(n) for a scan | O(d) retained state |
| Two pointers in sorted values | O(n) | O(1) auxiliary space |

## State and assumptions

For Two Sum, record earlier values only after lookup. For nearby duplicates, retain the latest occurrence and update after a failed distance check. Two-pointer elimination requires sorted values and distinct positions. For 3Sum, distinguish distinct positions from distinct output value triplets, and count copying, sorting, and output storage separately.

## Core sources

Erik Demaine and Srini Devadas, [Introduction to Algorithms, MIT 6.006](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/) (Fall 2011).

<!-- ko -->

## 연산 비용

n은 입력 길이, d는 서로 다른 값의 수, q는 복사하는 원소 수입니다. 정수 연산과 정수 해시는 상수 비용으로 봅니다.

| 연산 | 시간 | 저장 공간·조건 |
| --- | --- | --- |
| 리스트 인덱스 | O(1) | 위치로 바로 접근 |
| 리스트 membership | O(n) | 값의 순차 비교 |
| dict/set 조회·갱신 | 평균 O(1), 최악 O(n) | hashable 키; 긴 키의 해시 비용 별도 |
| q개 원소 복사 | O(q) | O(q) 얕은 참조 복사 |
| n개 정렬 | 최악 O(n log n) | Python 작업 공간 O(n) |
| 값마다 최근 위치 저장 | 한 번 순회 시 평균 O(n) | O(d) 상태 저장 |
| 정렬된 값의 두 포인터 | O(n) | 보조 공간 O(1) |

## 상태와 전제

Two Sum은 조회한 뒤 현재 값을 저장해 이전 위치만 비교합니다. 최근 중복은 거리 조건을 만족하지 않은 재등장도 최근 위치로 갱신합니다. 두 포인터의 후보 제거에는 정렬과 서로 다른 위치라는 조건이 필요합니다. 3Sum은 서로 다른 위치와 중복 없는 값 조합을 구분하고 복사·정렬·출력 비용을 따로 셉니다.

## 핵심 참고자료

Erik Demaine·Srini Devadas, [Introduction to Algorithms, MIT 6.006](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/) (2011년 가을 학기).
