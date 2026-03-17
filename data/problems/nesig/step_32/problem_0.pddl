(define (problem problem_0)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7 obj8 obj9 obj10 obj11 obj12 obj13 - block
)

(:init
	(clear obj0)
	(clear obj3)
	(clear obj7)
	(clear obj10)
	(clear obj12)
	(clear obj13)
	(handempty)
	(on obj2 obj1)
	(on obj3 obj2)
	(on obj5 obj4)
	(on obj6 obj5)
	(on obj7 obj6)
	(on obj9 obj8)
	(on obj10 obj9)
	(on obj12 obj11)
	(ontable obj0)
	(ontable obj1)
	(ontable obj4)
	(ontable obj8)
	(ontable obj11)
	(ontable obj13)
)

(:goal (and
	(on obj6 obj8)
	(on obj12 obj7)
))
)