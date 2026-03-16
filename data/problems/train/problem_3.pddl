

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b2)
(on b2 b5)
(on b3 b8)
(ontable b4)
(on b5 b9)
(on b6 b1)
(ontable b7)
(ontable b8)
(on b9 b10)
(on b10 b7)
(clear b3)
(clear b4)
(clear b6)
)
(:goal
(and
(on b1 b10)
(on b2 b1)
(on b3 b6)
(on b5 b4)
(on b7 b3)
(on b8 b7))
)
)


