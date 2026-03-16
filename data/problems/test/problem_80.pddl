

(define (problem BW-rand-6)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(on b3 b1)
(on b4 b5)
(ontable b5)
(on b6 b3)
(clear b2)
(clear b4)
(clear b6)
)
(:goal
(and
(on b1 b5)
(on b3 b2)
(on b4 b6)
(on b5 b3))
)
)


