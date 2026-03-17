(define (problem problem_20)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7 obj8 obj9 obj10 obj11 obj12 obj13 obj14 obj15 obj16 obj17 - block
)

(:init
	(clear obj2)
	(clear obj5)
	(clear obj7)
	(clear obj8)
	(clear obj10)
	(clear obj15)
	(clear obj17)
	(handempty)
	(on obj1 obj0)
	(on obj2 obj1)
	(on obj4 obj3)
	(on obj5 obj4)
	(on obj7 obj6)
	(on obj10 obj9)
	(on obj12 obj11)
	(on obj13 obj12)
	(on obj14 obj13)
	(on obj15 obj14)
	(on obj17 obj16)
	(ontable obj0)
	(ontable obj3)
	(ontable obj6)
	(ontable obj8)
	(ontable obj9)
	(ontable obj11)
	(ontable obj16)
)

(:goal (and
	(on obj4 obj3)
	(on obj13 obj4)
	(on obj14 obj6)
	(on obj15 obj8)
))
)