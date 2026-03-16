(define (problem problem_29)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7 obj8 obj9 obj10 obj11 obj12 obj13 obj14 obj15 obj16 obj17 obj18 - block
)

(:init
	(clear obj0)
	(clear obj3)
	(clear obj4)
	(clear obj8)
	(clear obj12)
	(clear obj14)
	(clear obj16)
	(clear obj18)
	(handempty)
	(on obj2 obj1)
	(on obj3 obj2)
	(on obj6 obj5)
	(on obj7 obj6)
	(on obj8 obj7)
	(on obj10 obj9)
	(on obj11 obj10)
	(on obj12 obj11)
	(on obj14 obj13)
	(on obj16 obj15)
	(on obj18 obj17)
	(ontable obj0)
	(ontable obj1)
	(ontable obj4)
	(ontable obj5)
	(ontable obj9)
	(ontable obj13)
	(ontable obj15)
	(ontable obj17)
)

(:goal (and
	(on obj7 obj5)
))
)