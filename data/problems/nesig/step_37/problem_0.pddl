(define (problem problem_0)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7 obj8 obj9 obj10 - block
)

(:init
	(clear obj0)
	(clear obj1)
	(clear obj2)
	(clear obj3)
	(clear obj4)
	(clear obj7)
	(clear obj8)
	(clear obj9)
	(clear obj10)
	(handempty)
	(on obj6 obj5)
	(on obj7 obj6)
	(ontable obj0)
	(ontable obj1)
	(ontable obj2)
	(ontable obj3)
	(ontable obj4)
	(ontable obj5)
	(ontable obj8)
	(ontable obj9)
	(ontable obj10)
)

(:goal (and
	(on obj0 obj5)
	(on obj2 obj1)
	(on obj3 obj0)
	(on obj6 obj7)
	(on obj7 obj9)
	(on obj8 obj4)
))
)