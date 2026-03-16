

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(on b3 b6)
(on b4 b7)
(on b5 b1)
(ontable b6)
(on b7 b2)
(on b8 b5)
(clear b3)
(clear b4)
(clear b8)
)
(:goal
(and
(on b1 b2)
(on b3 b5)
(on b5 b1)
(on b6 b3)
(on b7 b8))
)
)


