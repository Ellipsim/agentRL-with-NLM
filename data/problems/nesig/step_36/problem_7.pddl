(define (problem problem_7)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7 obj8 obj9 obj10 obj11 obj12 obj13 obj14 obj15 obj16 - block
)

(:init
	(clear obj1)
	(clear obj4)
	(clear obj5)
	(clear obj7)
	(clear obj11)
	(clear obj15)
	(clear obj16)
	(handempty)
	(on obj1 obj0)
	(on obj3 obj2)
	(on obj4 obj3)
	(on obj7 obj6)
	(on obj9 obj8)
	(on obj10 obj9)
	(on obj11 obj10)
	(on obj13 obj12)
	(on obj14 obj13)
	(on obj15 obj14)
	(ontable obj0)
	(ontable obj2)
	(ontable obj5)
	(ontable obj6)
	(ontable obj8)
	(ontable obj12)
	(ontable obj16)
)

(:goal (and
	(on obj13 obj12)
))
)