(define (problem problem_27)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7 obj8 obj9 obj10 - block
)

(:init
	(clear obj0)
	(clear obj2)
	(clear obj4)
	(clear obj6)
	(clear obj8)
	(clear obj9)
	(clear obj10)
	(handempty)
	(on obj2 obj1)
	(on obj4 obj3)
	(on obj6 obj5)
	(on obj8 obj7)
	(ontable obj0)
	(ontable obj1)
	(ontable obj3)
	(ontable obj5)
	(ontable obj7)
	(ontable obj9)
	(ontable obj10)
)

(:goal (and
	(on obj2 obj1)
	(on obj4 obj3)
))
)