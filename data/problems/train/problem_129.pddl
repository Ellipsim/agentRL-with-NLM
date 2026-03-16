

(define (problem BW-rand-7)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(on b1 b5)
(on b2 b4)
(ontable b3)
(on b4 b6)
(ontable b5)
(on b6 b3)
(on b7 b2)
(clear b1)
(clear b7)
)
(:goal
(and
(on b1 b7)
(on b3 b1)
(on b5 b4)
(on b6 b5)
(on b7 b2))
)
)


