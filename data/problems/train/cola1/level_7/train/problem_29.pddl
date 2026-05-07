

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b8)
(ontable b2)
(ontable b3)
(on b4 b3)
(ontable b5)
(on b6 b7)
(on b7 b4)
(on b8 b2)
(clear b1)
(clear b5)
(clear b6)
)
(:goal
(and
(on b1 b4)
(on b3 b5)
(on b4 b2)
(on b8 b7))
)
)


