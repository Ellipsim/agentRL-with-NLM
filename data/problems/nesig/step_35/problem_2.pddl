(define (problem problem_2)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7 obj8 obj9 obj10 obj11 obj12 - block
)

(:init
	(clear obj0)
	(clear obj1)
	(clear obj4)
	(clear obj5)
	(clear obj6)
	(clear obj7)
	(clear obj8)
	(clear obj9)
	(clear obj10)
	(clear obj11)
	(clear obj12)
	(handempty)
	(on obj3 obj2)
	(on obj4 obj3)
	(ontable obj0)
	(ontable obj1)
	(ontable obj2)
	(ontable obj5)
	(ontable obj6)
	(ontable obj7)
	(ontable obj8)
	(ontable obj9)
	(ontable obj10)
	(ontable obj11)
	(ontable obj12)
)

(:goal (and
	(on obj0 obj9)
	(on obj2 obj3)
	(on obj3 obj8)
	(on obj4 obj10)
	(on obj11 obj5)
))
)