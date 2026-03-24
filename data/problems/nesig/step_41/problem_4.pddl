(define (problem problem_4)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7 obj8 obj9 obj10 obj11 - block
)

(:init
	(clear obj0)
	(clear obj4)
	(clear obj5)
	(clear obj6)
	(clear obj7)
	(clear obj8)
	(clear obj9)
	(clear obj10)
	(clear obj11)
	(handempty)
	(on obj2 obj1)
	(on obj3 obj2)
	(on obj4 obj3)
	(ontable obj0)
	(ontable obj1)
	(ontable obj5)
	(ontable obj6)
	(ontable obj7)
	(ontable obj8)
	(ontable obj9)
	(ontable obj10)
	(ontable obj11)
)

(:goal (and
	(on obj1 obj2)
	(on obj2 obj3)
	(on obj3 obj7)
	(on obj4 obj11)
	(on obj6 obj8)
))
)