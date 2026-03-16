(define (problem problem_29)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7 obj8 obj9 obj10 obj11 obj12 obj13 - block
)

(:init
	(clear obj0)
	(clear obj2)
	(clear obj6)
	(clear obj7)
	(clear obj10)
	(clear obj13)
	(handempty)
	(on obj2 obj1)
	(on obj4 obj3)
	(on obj5 obj4)
	(on obj6 obj5)
	(on obj9 obj8)
	(on obj10 obj9)
	(on obj12 obj11)
	(on obj13 obj12)
	(ontable obj0)
	(ontable obj1)
	(ontable obj3)
	(ontable obj7)
	(ontable obj8)
	(ontable obj11)
)

(:goal (and
	(on obj2 obj13)
	(on obj4 obj3)
	(on obj5 obj4)
	(on obj9 obj8)
	(on obj12 obj11)
	(on obj13 obj12)
))
)