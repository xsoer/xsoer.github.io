package structs

import "fmt"

// func intersectionTest() {
// 	arr1 := [7]int{4, 2, 5, 3, 6, 1, 9}
// 	arr2 := [6]int{3, 8, 10, 4, 12, 7}

// 	for i := 0; i < len(arr1); i++ {
// 		fmt.Println(arr1[i])
// 	}
// 	for i := 0; i < len(arr2); i++ {
// 		fmt.Println(arr2[i])
// 	}
// 	intersection(arr1, arr2)
// }

func intersection(a []int, b []int) {
	same := 0
	for i := 0; i < len(a); i++ {
		for j := 0; j < len(b); j++ {
			if a[i] == b[j] {
				same++
			}
		}
	}
	fmt.Println(same)
}
