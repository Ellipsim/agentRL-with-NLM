

(define (problem BW-rand-7)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(on b1 b2)
(ontable b2)
(ontable b3)
(on b4 b1)
(on b5 b7)
(ontable b6)
(on b7 b6)
(clear b3)
(clear b4)
(clear b5)
)
(:goal
(and
(on b3 b1)
(on b4 b6)
(on b7 b3))
)
)


