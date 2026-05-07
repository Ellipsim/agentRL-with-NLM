

(define (problem BW-rand-7)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(on b1 b4)
(on b2 b3)
(ontable b3)
(ontable b4)
(on b5 b6)
(on b6 b1)
(on b7 b5)
(clear b2)
(clear b7)
)
(:goal
(and
(on b1 b2)
(on b3 b6)
(on b4 b1)
(on b5 b4)
(on b7 b3))
)
)


