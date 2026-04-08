(define (problem problem_2)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7 obj8 obj9 obj10 - block
)

(:init
	(clear obj0)
	(clear obj1)
	(clear obj5)
	(clear obj6)
	(clear obj7)
	(clear obj10)
	(handempty)
	(on obj3 obj2)
	(on obj4 obj3)
	(on obj5 obj4)
	(on obj9 obj8)
	(on obj10 obj9)
	(ontable obj0)
	(ontable obj1)
	(ontable obj2)
	(ontable obj6)
	(ontable obj7)
	(ontable obj8)
)

(:goal (and
	(on obj3 obj2)
	(on obj4 obj3)
	(on obj5 obj4)
	(on obj9 obj8)
	(on obj10 obj9)
))
)