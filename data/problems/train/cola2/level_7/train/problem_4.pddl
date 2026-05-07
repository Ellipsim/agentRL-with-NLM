

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b8)
(on b2 b3)
(on b3 b6)
(ontable b4)
(ontable b5)
(on b6 b1)
(ontable b7)
(on b8 b5)
(clear b2)
(clear b4)
(clear b7)
)
(:goal
(and
(on b1 b6)
(on b4 b5)
(on b5 b3)
(on b7 b1)
(on b8 b7))
)
)


