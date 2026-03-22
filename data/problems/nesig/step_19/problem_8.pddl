(define (problem problem_8)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 - block
)

(:init
	(clear obj3)
	(handempty)
	(on obj1 obj0)
	(on obj2 obj1)
	(on obj3 obj2)
	(ontable obj0)
)

(:goal (and
	(on obj1 obj0)
	(on obj2 obj1)
))
)