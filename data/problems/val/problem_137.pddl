

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(ontable b3)
(on b4 b5)
(ontable b5)
(on b6 b8)
(on b7 b3)
(on b8 b4)
(clear b1)
(clear b2)
(clear b6)
(clear b7)
)
(:goal
(and
(on b1 b5)
(on b2 b3)
(on b3 b4)
(on b4 b6)
(on b5 b8)
(on b8 b7))
)
)


