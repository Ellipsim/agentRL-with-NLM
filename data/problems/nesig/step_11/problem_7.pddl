(define (problem problem_7)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7 obj8 obj9 - block
)

(:init
	(clear obj1)
	(clear obj2)
	(clear obj4)
	(clear obj6)
	(clear obj7)
	(clear obj8)
	(clear obj9)
	(handempty)
	(on obj1 obj0)
	(on obj4 obj3)
	(on obj6 obj5)
	(ontable obj0)
	(ontable obj2)
	(ontable obj3)
	(ontable obj5)
	(ontable obj7)
	(ontable obj8)
	(ontable obj9)
)

(:goal (and
	(on obj1 obj0)
	(on obj6 obj5)
))
)