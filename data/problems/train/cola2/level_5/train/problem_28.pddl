

(define (problem BW-rand-7)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(on b1 b7)
(on b2 b1)
(ontable b3)
(ontable b4)
(ontable b5)
(on b6 b3)
(on b7 b6)
(clear b2)
(clear b4)
(clear b5)
)
(:goal
(and
(on b1 b2)
(on b2 b7)
(on b3 b6)
(on b4 b1)
(on b7 b3))
)
)


