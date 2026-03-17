(define (problem problem_24)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7 obj8 obj9 obj10 obj11 - block
)

(:init
	(clear obj0)
	(clear obj1)
	(clear obj3)
	(clear obj7)
	(clear obj8)
	(clear obj9)
	(clear obj11)
	(handempty)
	(on obj3 obj2)
	(on obj5 obj4)
	(on obj6 obj5)
	(on obj7 obj6)
	(on obj11 obj10)
	(ontable obj0)
	(ontable obj1)
	(ontable obj2)
	(ontable obj4)
	(ontable obj8)
	(ontable obj9)
	(ontable obj10)
)

(:goal (and
	(on obj6 obj11)
	(on obj11 obj4)
))
)