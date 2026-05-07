

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(on b3 b12)
(on b4 b5)
(on b5 b6)
(ontable b6)
(on b7 b11)
(on b8 b4)
(on b9 b8)
(ontable b10)
(on b11 b1)
(on b12 b2)
(clear b3)
(clear b7)
(clear b9)
(clear b10)
)
(:goal
(and
(on b1 b5)
(on b2 b4)
(on b3 b12)
(on b5 b2)
(on b6 b1)
(on b7 b6)
(on b8 b3)
(on b9 b8)
(on b11 b7))
)
)


