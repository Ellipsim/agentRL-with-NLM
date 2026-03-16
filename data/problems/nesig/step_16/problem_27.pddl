(define (problem problem_27)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7 obj8 obj9 obj10 obj11 obj12 obj13 obj14 obj15 obj16 - block
)

(:init
	(clear obj0)
	(clear obj4)
	(clear obj6)
	(clear obj8)
	(clear obj14)
	(clear obj16)
	(handempty)
	(on obj2 obj1)
	(on obj3 obj2)
	(on obj4 obj3)
	(on obj6 obj5)
	(on obj8 obj7)
	(on obj10 obj9)
	(on obj11 obj10)
	(on obj12 obj11)
	(on obj13 obj12)
	(on obj14 obj13)
	(on obj16 obj15)
	(ontable obj0)
	(ontable obj1)
	(ontable obj5)
	(ontable obj7)
	(ontable obj9)
	(ontable obj15)
)

(:goal (and
	(on obj10 obj9)
))
)