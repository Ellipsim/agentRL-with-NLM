(define (problem problem_8)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7 obj8 obj9 obj10 obj11 obj12 obj13 - block
)

(:init
	(clear obj1)
	(clear obj2)
	(clear obj5)
	(clear obj8)
	(clear obj9)
	(clear obj10)
	(clear obj13)
	(handempty)
	(on obj1 obj0)
	(on obj4 obj3)
	(on obj5 obj4)
	(on obj7 obj6)
	(on obj8 obj7)
	(on obj12 obj11)
	(on obj13 obj12)
	(ontable obj0)
	(ontable obj2)
	(ontable obj3)
	(ontable obj6)
	(ontable obj9)
	(ontable obj10)
	(ontable obj11)
)

(:goal (and
	(on obj1 obj4)
	(on obj4 obj3)
	(on obj7 obj6)
	(on obj12 obj11)
))
)