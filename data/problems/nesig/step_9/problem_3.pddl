(define (problem problem_3)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7 obj8 obj9 obj10 - block
)

(:init
	(clear obj2)
	(clear obj5)
	(clear obj7)
	(clear obj8)
	(clear obj10)
	(handempty)
	(on obj1 obj0)
	(on obj2 obj1)
	(on obj4 obj3)
	(on obj5 obj4)
	(on obj7 obj6)
	(on obj10 obj9)
	(ontable obj0)
	(ontable obj3)
	(ontable obj6)
	(ontable obj8)
	(ontable obj9)
)

(:goal (and
	(on obj0 obj9)
	(on obj1 obj10)
	(on obj2 obj8)
	(on obj4 obj3)
	(on obj5 obj4)
	(on obj7 obj5)
	(on obj10 obj2)
))
)