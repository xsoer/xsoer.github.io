package structs

import (
	"sync"
)

type Set struct {
	m map[interface{}]struct{}
	sync.RWMutex
}

var Exists = struct{}{}

func NewSet() *Set {
	return &Set{
		m: make(map[interface{}]struct{}),
	}
}

func (s *Set) Add(item interface{}) error {
	s.Lock()
	defer s.Unlock()
	s.m[item] = Exists
	return nil
}

func (s *Set) Remove(item interface{}) {
	s.Lock()
	s.Unlock()
	delete(s.m, item)
}

func (s *Set) Has(item interface{}) bool {
	s.RLock()
	defer s.RUnlock()
	_, ok := s.m[item]
	return ok
}

func (s *Set) Len() int {
	return len(s.m)
}

func (s *Set) Clear() {
	// s.Lock
	// defer s.Unlock()
	s.m = make(map[interface{}]struct{})
}

func (s *Set) IsEmpty() bool {
	if s.Len() == 0 {
		return true
	}
	return false
}

// func (s *Set) List() []int {
// 	s.RLock()
// 	defer s.RUnlock()
// 	list := []struct{}
// 	for item := range s.m {
// 		list = append(list, item)
// 	}
// 	return list
// }

// func main() {
// 	// 初始化
// 	s := New()

// 	s.Add(1)
// 	s.Add(1)
// 	s.Add(1)

// 	// s.Clear()
// 	// if s.IsEmpty() {
// 	// 	fmt.Println("0 item")
// 	// }

// 	s.Add(1)
// 	s.Add(2)
// 	s.Add(3)

// 	if s.Has(2) {
// 		fmt.Println("2 does exist")
// 	}

// 	// s.Remove(2)
// 	// s.Remove(3)
// 	fmt.Println(s.Len())
// 	// fmt.Println("list of all items", s.List())
// }
