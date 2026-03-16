

(define (problem BW-rand-7)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(on b1 b6)
(on b2 b1)
(ontable b3)
(on b4 b3)
(on b5 b7)
(on b6 b4)
(ontable b7)
(clear b2)
(clear b5)
)
(:goal
(and
(on b4 b5)
(on b5 b6)
(on b6 b3)
(on b7 b2))
)
)


