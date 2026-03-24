(define (problem problem_5)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7 obj8 obj9 obj10 obj11 obj12 - block
)

(:init
	(clear obj0)
	(clear obj1)
	(clear obj5)
	(clear obj7)
	(clear obj9)
	(clear obj10)
	(clear obj11)
	(clear obj12)
	(handempty)
	(on obj3 obj2)
	(on obj4 obj3)
	(on obj5 obj4)
	(on obj7 obj6)
	(on obj9 obj8)
	(ontable obj0)
	(ontable obj1)
	(ontable obj2)
	(ontable obj6)
	(ontable obj8)
	(ontable obj10)
	(ontable obj11)
	(ontable obj12)
)

(:goal (and
	(on obj1 obj2)
	(on obj2 obj3)
	(on obj3 obj9)
	(on obj4 obj5)
	(on obj5 obj10)
	(on obj6 obj7)
	(on obj7 obj8)
	(on obj9 obj11)
))
)